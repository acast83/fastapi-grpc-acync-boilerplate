import services.grpc.users.proto.users_pb2 as users_pb2
from .conftest import BaseTest, HTTPMethod


class TestsUsersBasic(BaseTest):
    request = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "test@test.com",
        "username": "test",
        "password": "test"
    }
    create_user_request = users_pb2.CreateUserRequest(**request)
    login_user_request = users_pb2.LoginUserRequest(username=request["username"], password=request["password"])

    async def test_health(self):
        res = await self.api_call(url="/api-gateway/health/", method=HTTPMethod.GET)
        assert res == {'healthy': True}

    async def test_create_user(self):
        new_user = await self.user_service_stub.CreateUser(request=self.create_user_request)
        assert new_user.username == self.create_user_request.username
        self.user_id = new_user.id
        self.user = new_user

    async def test_create_user_api(self):
        create_user_response = await self.api_call(url="/api-gateway/users/register",
                                                   method=HTTPMethod.POST, body=self.request)
        assert create_user_response["username"] == self.request["username"]
        assert create_user_response["id"] is not None
        assert create_user_response["token"] is not None
        self.user_id = create_user_response["id"]

        await self.api_call(url="/api-gateway/users/register",
                            method=HTTPMethod.POST,
                            body=self.request, expected_status_code=406)

    async def test_login_user_api(self):
        await self.test_create_user_api()

        await self.api_call(url="/api-gateway/users/login",
                            method=HTTPMethod.POST,
                            body={"username": "test123",
                                  "password": "test"
                                  },
                            expected_status_code=401)

        await self.api_call(url="/api-gateway/users/login",
                            method=HTTPMethod.POST,
                            body={"username": "test",
                                  "password": "test123"
                                  },
                            expected_status_code=401)

        login_user_response = await self.api_call(url="/api-gateway/users/login",
                                                  method=HTTPMethod.POST,
                                                  body={"username": self.request["username"],
                                                        "password": self.request["password"]
                                                        }, expected_status_code=200)

        assert self.user_id == login_user_response["id"]

    async def test_login_user(self):
        await self.test_create_user()

        response = await self.user_service_stub.LoginUser(request=self.login_user_request)
        assert response.id == self.user_id
        self.token = response.token

    async def test_get_current_user(self):
        await self.test_login_user()
        current_user = await self.user_service_stub.GetCurrentUser(request=users_pb2.GetCurrentUserRequest(token=self.token))
        assert current_user.username == self.request["username"]
        assert current_user.first_name == self.request["first_name"]
        assert current_user.last_name == self.request["last_name"]
