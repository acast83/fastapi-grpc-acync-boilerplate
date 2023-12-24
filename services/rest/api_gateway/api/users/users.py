import grpc
from fastapi import APIRouter, HTTPException

import services.grpc.users.proto.users_pb2 as users_pb2
from core.utils.grpc import grpc_response_to_dict
from services.grpc.users.service.users_service import UserService
from ...schemas.users.requests.user_requests import UserCreateRequest, UserLoginRequest

router = APIRouter()


@router.get('/about')
async def about() -> dict:
    return {"service": "users"}


@router.post('/register')
async def register_user(user: UserCreateRequest) -> dict:
    grpc_request = users_pb2.CreateUserRequest(**user.model_dump())

    try:
        return grpc_response_to_dict(await UserService.users_stub.CreateUser(request=grpc_request))
    except grpc.RpcError as e:
        status_code = e.code()
        details = e.details()
        # Map gRPC error to HTTP error
        if status_code == grpc.StatusCode.ALREADY_EXISTS:
            raise HTTPException(status_code=406, detail=details)
        else:
            # Handle other gRPC errors or use a generic error message
            raise HTTPException(status_code=500, detail="Internal server error")


@router.post('/login')
async def login_user(user: UserLoginRequest) -> dict:
    grpc_request = users_pb2.LoginUserRequest(**user.model_dump())

    try:
        return grpc_response_to_dict(await UserService.users_stub.LoginUser(request=grpc_request))
    except grpc.RpcError as e:
        status_code = e.code()
        details = e.details()
        # Map gRPC error to HTTP error
        if status_code == grpc.StatusCode.UNAUTHENTICATED:
            raise HTTPException(status_code=401, detail=details)
        else:
            # Handle other gRPC errors or use a generic error message
            raise HTTPException(status_code=500, detail="Internal server error")
