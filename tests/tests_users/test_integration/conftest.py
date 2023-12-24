import os
import pprint
from enum import Enum
from typing import List, Dict, AnyStr, Callable, Any, Type

import grpc
import psycopg2
import pydantic
from fastapi import status, Request, Depends
from httpx import Response, AsyncClient
from pytest import fixture

from core.application.monolith import monolith_app
from core.configuration.environments import set_env_variables
from core.database.db_credentials import DbCredentials
from core.database.db_setup import init_tortoise_for_services, close_connections
from core.handler.handler import Handler
from core.logging.logging_setup import get_test_logger, setup_logging
from services.grpc.activity_log.proto import activity_log_pb2_grpc as activity_log_pb2_grpc
from services.grpc.activity_log.service.activity_log_service import ActivityLogService
from services.grpc.lookups.proto import lookups_pb2_grpc as lookups_pb2_grpc
from services.grpc.lookups.service.lookups_service import LookupsService
from services.grpc.users.proto import users_pb2_grpc as users_pb2_grpc
from services.grpc.users.service.users_service import UserService


class HTTPMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class BaseTest:
    app = monolith_app
    last_result: Any = None
    handler: Handler = None
    user_service_stub = None
    activity_log_service_stub = None
    lookups_service_stub = None

    @staticmethod
    def get_handler():
        handler = Handler(log=get_test_logger(),
                          request=Depends(Request)
                          )
        return handler

    @fixture(autouse=True)
    async def setup(self) -> None:
        """
        Pytest fixture to set up the testing environment before each test case.
        """
        os.environ["test_mode"] = "true"
        self.handler = self.get_handler()
        set_env_variables()
        setup_logging()
        await self.drop_and_create_db()
        await init_tortoise_for_services()
        self.app.test_mode = True

        # grpc server side
        server = grpc.aio.server()
        user_service = UserService()
        activity_log_service = ActivityLogService()
        lookups_service = LookupsService()

        users_pb2_grpc.add_UserServiceServicer_to_server(user_service, server)
        activity_log_pb2_grpc.add_ActivityLogServiceServicer_to_server(activity_log_service, server)
        lookups_pb2_grpc.add_LookupsServiceServicer_to_server(lookups_service, server)

        port = server.add_insecure_port('localhost:0')
        # os.environ['GRPC_TEST_PORT'] = str(port)

        await server.start()

        # grpc client side
        channel = grpc.aio.insecure_channel(f'localhost:{port}')
        self.user_service_stub = users_pb2_grpc.UserServiceStub(channel)
        self.activity_log_service_stub = activity_log_pb2_grpc.ActivityLogServiceStub(channel)
        self.lookups_service_stub = lookups_pb2_grpc.LookupsServiceStub(channel)

        # this part enables ipc communication
        user_service.set_users_stub(self.user_service_stub)
        user_service.set_activity_log_stub(self.activity_log_service_stub)
        user_service.set_lookups_stub(self.lookups_service_stub)

        yield

        # After the test, stop the server and close the channel
        await server.stop(None)
        await channel.close()

        await close_connections()

    @staticmethod
    async def drop_and_create_db():

        db_cred = DbCredentials()

        test_db = f"test_{db_cred.application}"
        terminate_sessions_sql = f"""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = '{test_db}'
            AND pid <> pg_backend_pid();
        """

        conn = psycopg2.connect(user=db_cred.db_username,
                                password=db_cred.db_password,
                                database='template1', host='localhost')

        # Set the connection to autocommit mode
        conn.set_session(autocommit=True)

        cur = conn.cursor()
        cur.execute(terminate_sessions_sql)

        try:
            cur.execute(f"DROP DATABASE IF EXISTS {test_db}")
            cur.execute(f"CREATE DATABASE {test_db}")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_client_function(client: AsyncClient, method: HTTPMethod) -> Callable:
        """
        Maps an HTTP method to the corresponding httpx.AsyncClient method.

        :param client: The httpx.AsyncClient instance.
        :param method: The HTTP method as an HTTPMethod enum.
        :return: The callable httpx method.
        """
        client_function_map = {
            HTTPMethod.GET: client.get,
            HTTPMethod.POST: client.post,
            HTTPMethod.PATCH: client.patch,
            HTTPMethod.PUT: client.put,
            HTTPMethod.DELETE: client.delete
        }
        return client_function_map[method]

    async def api_call(self, url: str, method: HTTPMethod,
                       token: str = None,
                       body: List | Dict | AnyStr = None,
                       expected_status_code: int = None,
                       response_schema: Type[pydantic.BaseModel] = None
                       ) -> Dict | List | AnyStr | pydantic.BaseModel | None:
        """
        Makes an API call to the specified endpoint using the given method and body.


        :param url: The endpoint URL.
        :param method: The HTTP method as an HTTPMethod enum.
        :param token: Jwt token.
        :param body: The request body.
        :param expected_status_code: The expected HTTP status code.
        :param response_schema: pydantic schema
        :return: An ApiResponse instance with the response data and status code.
        """
        if method not in HTTPMethod:
            raise ValueError(f"Invalid HTTP method: {method}")
        success_status_codes = (status.HTTP_200_OK, status.HTTP_201_CREATED, status.HTTP_204_NO_CONTENT)

        async with AsyncClient(app=self.app, base_url="http://test") as client:
            client_funct = self.get_client_function(client=client, method=method)
            params = {"url": f"/api{url}"}
            if method in (HTTPMethod.POST, HTTPMethod.PUT, HTTPMethod.PATCH):
                params["json"] = body
            if token:
                params["headers"] = {"Authorization": f"Bearer {token}"}
            response: Response = await client_funct(**params)

        if expected_status_code:
            if response.status_code != expected_status_code:
                raise AssertionError("Unexpected status code returned.")
            if response.status_code not in success_status_codes:
                return
        else:
            if response.status_code not in success_status_codes:
                raise AssertionError("Response status code is not successful.")

        self.last_result = response.json()
        if response_schema:
            if isinstance(self.last_result, list):
                return [response_schema(**i) for i in self.last_result]
            return response_schema(**self.last_result)
        return self.last_result

    def print_last_result(self) -> None:
        """
        Prints the last API response result in a formatted manner.
        """
        print("\n" + "#" * 50)
        pprint.pprint(self.last_result)
        print("#" * 50 + "\n")
