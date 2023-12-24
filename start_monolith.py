import os

import grpc
import uvicorn

from core.application.monolith import monolith_app, list_all_routes
from core.configuration.environments import set_env_variables
from core.database.db_setup import init_tortoise_for_services, close_connections
from core.logging.logging_setup import setup_logging
from services.grpc.activity_log.proto import activity_log_pb2_grpc as activity_log_pb2_grpc
from services.grpc.activity_log.service.activity_log_service import ActivityLogService
from services.grpc.lookups.proto import lookups_pb2_grpc as lookups_pb2_grpc
from services.grpc.lookups.service.lookups_service import LookupsService
from services.grpc.users.proto import users_pb2_grpc as users_pb2_grpc
from services.grpc.users.service.users_service import UserService

set_env_variables()
setup_logging()

grpc_server = None
channel = None


async def setup_grpc() -> None:
    global grpc_server
    global channel
    grpc_server = grpc.aio.server()

    user_service = UserService()
    activity_log_service = ActivityLogService()
    lookups_service = LookupsService()

    users_pb2_grpc.add_UserServiceServicer_to_server(user_service, grpc_server)
    activity_log_pb2_grpc.add_ActivityLogServiceServicer_to_server(activity_log_service, grpc_server)
    lookups_pb2_grpc.add_LookupsServiceServicer_to_server(lookups_service, grpc_server)

    grpc_port = os.getenv("GRPC_PORT", None)
    assert grpc_port is not None
    grpc_server.add_insecure_port(f'localhost:{grpc_port}')
    # grpc_server.add_insecure_port(f'[::]:{grpc_port}')

    await grpc_server.start()

    channel = grpc.aio.insecure_channel(f'localhost:{grpc_port}')
    # Set stubs
    user_service.set_users_stub(users_pb2_grpc.UserServiceStub(channel))
    user_service.set_activity_log_stub(activity_log_pb2_grpc.ActivityLogServiceStub(channel))
    user_service.set_lookups_stub(lookups_pb2_grpc.LookupsServiceStub(channel))


@monolith_app.on_event("startup")
async def on_startup() -> None:
    """
    Startup event handler to list all routes when the application starts.

    When the FastAPI application starts, this async function is executed, and it calls
    the list_all_routes function to print out all the routes of the application.
    """
    if not os.getenv("skip", None) == "skip":
        await init_tortoise_for_services()
        await setup_grpc()
        list_all_routes(monolith_app)
        os.environ["skip"] = "skip"

    # await setup_grpc()


@monolith_app.on_event("shutdown")
async def on_shutdown() -> None:
    global grpc_server
    global channel
    if grpc_server:
        await grpc_server.stop(0)
    if channel:
        await channel.close()

    await close_connections()


monolith_app_host = os.getenv("MONOLITH_APP_HOST", None)
monolith_app_port = int(os.getenv("MONOLITH_APP_PORT"))

# The entry point for running the ASGI application.
if __name__ == "__main__":
    # uvicorn.run() starts the Uvicorn server with the specified application (monolith_app),
    # host address, port number, and reload option.

    uvicorn.run("start_monolith:monolith_app",
                host=monolith_app_host,
                port=monolith_app_port, reload=True)
