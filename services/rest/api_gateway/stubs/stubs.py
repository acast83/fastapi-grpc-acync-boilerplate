import os
import grpc
from fastapi import Request
import services.grpc.users.proto.users_pb2_grpc as users_pb2_grpc
import services.grpc.activity_log.proto.activity_log_pb2_grpc as activity_log_pb2_grpc
import services.grpc.lookups.proto.lookups_pb2_grpc as lookups_pb2_grpc

from core.services.services import extract_service_name

services_map = {
    'users': users_pb2_grpc.UserServiceStub,
    'activity_log': activity_log_pb2_grpc.ActivityLogServiceStub,
    'lookups': lookups_pb2_grpc.LookupsServiceStub
}


async def get_service_stub(request: Request):
    service_name = extract_service_name(request.url.path)
    if os.getenv('test_mode', "false") == "true":
        grpc_port = os.getenv('GRPC_TEST_PORT', 'default_grpc_port')

    else:
        grpc_port = os.getenv('GRPC_PORT', None)
        assert grpc_port is not None

    channel = grpc.aio.insecure_channel(f'localhost:{grpc_port}')
    return services_map[service_name](channel)
