from .conftest import BaseTest, HTTPMethod

import services.grpc.activity_log.proto.activity_log_pb2 as activity_log_pb2


class TestsActivityLogBasic(BaseTest):
    request = {
        "description": "test message",
    }
    create_message_request = activity_log_pb2.CreateMessageRequest(**request)

    async def test_health(self):
        res = await self.api_call(url="/api-gateway/health/", method=HTTPMethod.GET)
        assert res == {'healthy': True}

    async def test_create_message(self):
        new_message = await self.activity_log_service_stub.CreateMessage(request=self.create_message_request)
        assert new_message.description == self.create_message_request.description
        self.message_id = new_message.id
        self.message = new_message
