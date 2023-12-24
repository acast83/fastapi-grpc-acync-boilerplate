import asyncio

import grpc

from core.configuration.configuration import load_configuration
from core.configuration.environments import set_env_variables
from core.database.db_setup import init_tortoise_for_services, close_connections
from core.logging.logging_setup import setup_logging
from services.grpc.activity_log.proto import activity_log_pb2_grpc as activity_log_pb2_grpc
from services.grpc.activity_log.service.activity_log_service import ActivityLogService

# Global variables for server and channel
grpc_server = None
channel = None

set_env_variables()
setup_logging()

# Shutdown event
shutdown_event = asyncio.Event()


async def start_server() -> None:
    global grpc_server
    global channel

    await init_tortoise_for_services()

    configuration = load_configuration()

    grpc_server = grpc.aio.server()

    # Add service implementations to the server
    activity_log_service = ActivityLogService()

    activity_log_pb2_grpc.add_ActivityLogServiceServicer_to_server(activity_log_service, grpc_server)
    # Add other services if needed

    grpc_port = configuration["services"]["grpc"]["activity_log"]["port"]
    assert grpc_port is not None

    grpc_server.add_insecure_port(f'[::]:{grpc_port}')

    await grpc_server.start()

    # Setup channel and stubs
    channel = grpc.aio.insecure_channel(f'[::]:{grpc_port}')

    # Wait for the shutdown signal
    await shutdown_event.wait()

    # Shutdown actions
    await grpc_server.stop(None)  # Gracefully stop the server
    await channel.close()  # Close the channel
    await close_connections()


async def shutdown_signal() -> None:
    try:
        await asyncio.Future()  # Run forever until a KeyboardInterrupt occurs
    except KeyboardInterrupt:
        shutdown_event.set()  # Signal the server to shut down


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(start_server())
    loop.run_until_complete(shutdown_signal())
    loop.close()
