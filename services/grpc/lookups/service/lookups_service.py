import logging

import services.grpc.lookups.proto.lookups_pb2 as lookups_pb2
from core.service.base_service import BaseService
from services.grpc.lookups.proto.lookups_pb2_grpc import LookupsServiceServicer
from ..models import Lookups
from ..repositories.lookups_repository import LookupsRepository

logger = logging.getLogger("users")


# @class_exception_traceback_logging(logger)


class LookupsService(LookupsServiceServicer, BaseService[Lookups]):
    lookups_stub = None

    def __init__(self):
        super().__init__(repository=LookupsRepository(model=Lookups))
        self.lookups_repository = LookupsRepository(model=Lookups)

    @classmethod
    def set_lookups_stub(cls, stub):
        cls.lookups_stub = stub

    async def GetLookups(self, request, context) -> lookups_pb2.LookupResponse:
        return lookups_pb2.LookupResponse(**{"results": ["users", "lookups", "activity_log"]})
