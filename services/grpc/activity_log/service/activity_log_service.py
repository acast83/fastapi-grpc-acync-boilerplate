import logging
from typing import TypeVar

import services.grpc.activity_log.proto.activity_log_pb2 as pb2
from core.service.base_service import BaseService
from services.grpc.activity_log.proto.activity_log_pb2_grpc import ActivityLogServiceServicer
from services.rest.api_gateway.schemas.users.responses.user_responses import *
from ..models import Message
from ..repositories.activity_log_repository import ActivityLogRepository

ResponseSchema = TypeVar("ResponseSchema", bound=UserResponseBase)

logger = logging.getLogger("activity_log")


# @class_exception_traceback_logging(logger)

class ActivityLogService(ActivityLogServiceServicer, BaseService[Message], ):
    activity_log_stub = None

    def __init__(self):
        super().__init__(repository=ActivityLogRepository(model=Message))
        self.activity_log_repository = ActivityLogRepository(model=Message)

    @classmethod
    def set_activity_log_stub(cls, stub) -> None:
        cls.activity_log_stub = stub

    async def CreateMessage(self, request, context) -> pb2.CreateMessageResponse:
        logger.info("usao u CreateMessage, servis activity log")

        db_activity_log = await self.repository.create_in_db(attributes={"description": request.description})

        resu = pb2.CreateMessageResponse(id=str(db_activity_log.id),
                                         description=db_activity_log.description,
                                         )
        return resu
