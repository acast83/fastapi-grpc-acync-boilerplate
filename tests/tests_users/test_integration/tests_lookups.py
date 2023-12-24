from .conftest import BaseTest, HTTPMethod

import services.grpc.lookups.proto.lookups_pb2 as lookups_pb2


class TestsActivityLogBasic(BaseTest):
    request = {
        "query": "",
    }
    lookups_request = lookups_pb2.LookupRequest(**request)

    async def test_fetch_lookups(self):
        lookups_response = await self.lookups_service_stub.GetLookups(request=self.lookups_request)
        assert lookups_response.results == ["users", "lookups", "activity_log"]
