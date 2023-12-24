from pytest import fixture

# from services.grpc.users.controllers.users_controller import UserController
from services.grpc.users.models import User
from services.grpc.users.repositories.users_repository import UserRepository
from services.rest.api_gateway.schemas.users.requests.user_requests import UserCreateRequest, UserLoginRequest
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


class TestsUsersControllerBasic(TestsUsers):

    async def test_create_user(self):
        user_schema_response = await self.user_controller.create_user(user=self.user_schema_request)
        assert self.user_schema_request.username == user_schema_response.username
        assert self.user_schema_request.first_name == user_schema_response.first_name
        assert self.user_schema_request.last_name == user_schema_response.last_name
        self.id_user = user_schema_response.id

    async def test_login_user(self):
        await self.test_create_user()
        user_schema_request = UserLoginRequest(**{
            "username": self.user_schema_request.username,
            "password": self.user_schema_request.password
        })
        user_schema_response = await self.user_controller.login_user(user=user_schema_request)
        assert self.id_user == user_schema_response.id


class TestsUsersRepositoryBasic(TestsUsers):
    async def create_user_in_db(self):
        db_data = self.user_schema_request.model_dump()
        self.db_user: User = await self.user_repository.create_in_db(db_data)

    async def test_get_display_name_for_user(self):
        await self.create_user_in_db()
        await self.user_repository.update_display_name(self.db_user)
        await self.db_user.refresh_from_db()
        first_name = self.user_schema_request.first_name
        last_name = self.user_schema_request.last_name
        assert self.db_user.display_name == f"{first_name} {last_name}"

    async def test_get_search_field_for_user(self):
        await self.create_user_in_db()
        await self.user_repository.update_search_field(self.db_user)
        await self.db_user.refresh_from_db()
        search_field_data = (self.db_user.username,
                             self.user_schema_request.first_name,
                             self.user_schema_request.last_name,
                             self.user_schema_request.phone_number,
                             self.user_schema_request.email,
                             )
        search_field_data = f' {" ".join(search_field_data)}'
        assert self.db_user.search_field == search_field_data
