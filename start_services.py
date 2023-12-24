import os
import subprocess
import time

import grpc

from core.configuration.configuration import load_configuration
from core.configuration.environments import set_env_variables
from core.logging.logging_setup import setup_logging
from services.grpc.activity_log.proto import activity_log_pb2_grpc as activity_log_pb2_grpc
from services.grpc.activity_log.service.activity_log_service import ActivityLogService
from services.grpc.lookups.proto import lookups_pb2_grpc as lookups_pb2_grpc
from services.grpc.lookups.service.lookups_service import LookupsService
from services.grpc.users.proto import users_pb2_grpc as users_pb2_grpc
from services.grpc.users.service.users_service import UserService

set_env_variables()
setup_logging()

users_channel = None
activity_log_channel = None
lookups_channel = None


async def setup_grpc_clients() -> None:
    global users_channel
    global activity_log_channel
    global lookups_channel

    configuration = load_configuration()

    app_host = os.getenv("MS_APP_HOST", None)
    assert app_host is not None

    user_service = UserService()
    activity_log_service = ActivityLogService()
    lookups_service = LookupsService()

    grpc_port = os.getenv("GRPC_PORT", None)
    assert grpc_port is not None

    users_grpc_port = configuration["services"]["grpc"]["users"]["port"]
    assert users_grpc_port is not None

    users_app_host = app_host if app_host == "localhost" else "users"
    users_port = configuration["services"]["grpc"]["users"]["port"]
    users_channel = grpc.aio.insecure_channel(f'{users_app_host}:{users_port}')

    activity_log_app_host = app_host if app_host == "localhost" else "activity_log"
    activity_log_port = configuration["services"]["grpc"]["activity_log"]["port"]
    activity_log_channel = grpc.aio.insecure_channel(f'{activity_log_app_host}:{activity_log_port}')

    lookups_app_host = app_host if app_host == "localhost" else "lookups"
    lookups_port = configuration["services"]["grpc"]["lookups"]["port"]
    lookups_channel = grpc.aio.insecure_channel(f'{lookups_app_host}:{lookups_port}')

    # Set stubs for users service
    user_service.set_users_stub(users_pb2_grpc.UserServiceStub(users_channel))
    user_service.set_activity_log_stub(activity_log_pb2_grpc.ActivityLogServiceStub(activity_log_channel))
    user_service.set_lookups_stub(lookups_pb2_grpc.LookupsServiceStub(lookups_channel))

    # set stub for activity log
    activity_log_service.set_activity_log_stub(activity_log_pb2_grpc.ActivityLogServiceStub(activity_log_channel))

    # set stub for lookups
    lookups_service.set_lookups_stub(lookups_pb2_grpc.LookupsServiceStub(lookups_channel))
    ...


def start_services() -> None:
    config = load_configuration()
    for service_name in config["services"]["grpc"]:
        subprocess.Popen(f"python services/grpc/{service_name}/start_service.py", shell=True)
    for service_name in config["services"]["rest"]:
        subprocess.Popen(f"python services/rest/{service_name}/start_service.py", shell=True)
    while True:
        time.sleep(1000)


monolith_app_host = os.getenv("MONOLITH_APP_HOST", None)
monolith_app_port = int(os.getenv("MONOLITH_APP_PORT"))

if __name__ == "__main__":
    start_services()
