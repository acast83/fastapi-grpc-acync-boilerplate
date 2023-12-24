from pytest import fixture

from services.grpc.users.controllers import UserController
from services.grpc.users.models import User
from services.grpc.users.repositories import UserRepository
from services.rest.api_gateway.schemas.users.requests.user_requests import UserCreateRequest
from services.grpc.users.service.users_service import UserService
from ...conftest import BaseTest


class TestsUsers(BaseTest):
    user_repository = None
    user_controller = None
    user_schema_request = None

    @fixture(autouse=True)
    async def get_user_controller(self) -> None:
        self.user_repository = UserRepository(model=User, handler=self.handler)
        self.user_controller = UserController(user_repository=self.user_repository,
                                              user_service=UserService(),
                                              handler=self.handler
                                              )
        self.user_schema_request = UserCreateRequest(**{"username": "test_user",
                                                        "first_name": "test",
                                                        "last_name": "test",
                                                        "password": "test_pass",
                                                        "phone_number": "555-666",
                                                        "email": "test@test.com"
                                                        })
