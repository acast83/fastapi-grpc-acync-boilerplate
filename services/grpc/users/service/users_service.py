import logging

from fastapi import HTTPException, status
from grpc import StatusCode
from passlib.hash import bcrypt

import services.grpc.activity_log.proto.activity_log_pb2 as al_pb2
import services.grpc.lookups.proto.lookups_pb2 as lookups_pb2
import services.grpc.users.proto.users_pb2 as users_pb2
from core.security.authentication import TokenUtils
from core.service.base_service import BaseService
from services.grpc.users.proto.users_pb2_grpc import UserServiceServicer
from ..models import User
from ..repositories.users_repository import UserRepository

logger = logging.getLogger("users")


# from core.logging.logging_setup import class_exception_traceback_logging
# @class_exception_traceback_logging(logger)

class UserService(UserServiceServicer, BaseService[User]):
    users_stub = None
    activity_log_stub = None
    lookups_stub = None

    def __init__(self):

        BaseService.__init__(self, repository=UserRepository(model=User))
        self.user_repository = UserRepository(model=User)
        self.lookups_request = lookups_pb2.LookupRequest()

    @classmethod
    def set_users_stub(cls, stub) -> None:
        cls.users_stub = stub

    @classmethod
    def set_activity_log_stub(cls, stub) -> None:
        cls.activity_log_stub = stub

    @classmethod
    def set_lookups_stub(cls, stub) -> None:
        cls.lookups_stub = stub

    async def CreateUser(self, request, context) -> users_pb2.CreateUserResponse:

        if self.activity_log_stub:
            try:
                log_request = al_pb2.CreateMessageRequest(description="User created")
                await self.activity_log_stub.CreateMessage(log_request)
            except Exception as e:
                raise

        if await self.repository.get_single_by_params(query_params={"username": request.username},
                                                      raise_error=False):
            context.set_code(StatusCode.ALREADY_EXISTS)
            context.set_details("USER_ALREADY_EXISTS")
            return users_pb2.CreateUserResponse()

        # sluzi mi samo za testiranje ipc komunikacije
        # lookups = await self.lookups_stub.GetLookups(request=self.lookups_request)

        db_data = {"username": request.username, "password": self.hash_password(request.password),
                   "first_name": request.first_name, "last_name": request.last_name,
                   "email": request.email}

        db_user = await self.repository.create_in_db(attributes=db_data)
        await self.user_repository.update_user_display_and_search(user=db_user)
        token = TokenUtils().encode_token(data={"id": str(db_user.id),
                                                "username": db_user.username
                                                })

        return users_pb2.CreateUserResponse(id=str(db_user.id), username=db_user.username, token=token)

    async def LoginUser(self, request, context) -> users_pb2.LoginUserResponse:
        db_user: User = await self.repository.get_single_by_params({"username": request.username},
                                                                   raise_error=False)
        if not db_user:
            context.set_code(StatusCode.UNAUTHENTICATED)
            context.set_details("INVALID_CREDENTIALS")
            return users_pb2.LoginUserResponse()

        if not self.verify_password(request.password, db_user.password):
            context.set_code(StatusCode.UNAUTHENTICATED)
            context.set_details("INVALID_CREDENTIALS")
            return users_pb2.LoginUserResponse()

        if self.activity_log_stub:
            log_request = al_pb2.CreateMessageRequest(description=f"User {db_user.username} was logged in")
            await self.activity_log_stub.CreateMessage(log_request)

        token = TokenUtils().encode_token(data={"id": str(db_user.id),
                                                "username": db_user.username
                                                })
        return users_pb2.LoginUserResponse(id=str(db_user.id), token=token)

    async def UpdateUser(self, request, context):
        pass

    async def GetCurrentUser(self, request, context) -> users_pb2.GetCurrentUserResponse:

        if not request.token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="DATA_MISSING_FROM_REQUEST_TOKEN")
        token_data = TokenUtils().decode_token(token=request.token)
        db_user = await self.repository.get_single_by_params(query_params={"id": token_data["id_user"]})

        return users_pb2.GetCurrentUserResponse(id=str(db_user.id), username=db_user.username, first_name=db_user.first_name,
                                                last_name=db_user.last_name, email=db_user.email)

    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hash(password)

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        return bcrypt.verify(password, hashed_password)
