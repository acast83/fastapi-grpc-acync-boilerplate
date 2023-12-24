import asyncio
import logging
import os

import grpc

from core.configuration.configuration import load_configuration
from core.configuration.environments import set_env_variables
from core.database.db_setup import init_tortoise_for_services, close_connections
from core.logging.logging_setup import setup_logging
from services.grpc.activity_log.proto import activity_log_pb2_grpc as activity_log_pb2_grpc
from services.grpc.lookups.proto import lookups_pb2_grpc as lookups_pb2_grpc
from services.grpc.users.proto import users_pb2_grpc as users_pb2_grpc
from services.grpc.users.service.users_service import UserService

setup_logging()
set_env_variables()

grpc_server = None
channel = None

# Shutdown event
shutdown_event = asyncio.Event()

logger = logging.getLogger("users")

logger.info("called users start service module")


async def start_server():
    await init_tortoise_for_services()

    logger.info("got into start server")

    configuration = load_configuration()

    app_host = os.getenv("MS_APP_HOST", None)
    assert app_host is not None

    grpc_server = grpc.aio.server()

    user_service = UserService()

    users_pb2_grpc.add_UserServiceServicer_to_server(user_service, grpc_server)

    users_grpc_port = configuration["services"]["grpc"]["users"]["port"]
    assert users_grpc_port is not None
    grpc_server.add_insecure_port(f'localhost:{users_grpc_port}')

    await grpc_server.start()
    logger.info("server started")

    activity_log_app_host = app_host if app_host == "localhost" else "activity_log"
    activity_log_port = configuration["services"]["grpc"]["activity_log"]["port"]
    activity_log_channel = grpc.aio.insecure_channel(f'{activity_log_app_host}:{activity_log_port}')

    lookups_app_host = app_host if app_host == "localhost" else "lookups"
    lookups_port = configuration["services"]["grpc"]["lookups"]["port"]
    lookups_channel = grpc.aio.insecure_channel(f'{lookups_app_host}:{lookups_port}')

    # Set stubs
    user_service.set_activity_log_stub(activity_log_pb2_grpc.ActivityLogServiceStub(activity_log_channel))
    user_service.set_lookups_stub(lookups_pb2_grpc.LookupsServiceStub(lookups_channel))

    # Wait for the shutdown signal
    logger.info("added stubs to user service")

    await shutdown_event.wait()

    # Shutdown actions
    await grpc_server.stop(None)  # Gracefully stop the server
    await activity_log_channel.close()
    await lookups_channel.close()
    await close_connections()


async def shutdown_signal():
    try:
        await asyncio.Future()  # Run forever until a KeyboardInterrupt occurs
    except KeyboardInterrupt:
        shutdown_event.set()  # Signal the server to shut down


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(start_server())
    loop.run_until_complete(shutdown_signal())
    loop.close()
