import logging
import uuid
from logging import Logger

from fastapi import Request

from core.security.authentication import TokenUtils
from core.services.services import get_service_name


class Handler:
    def __init__(self, request: Request,
                 log: Logger,
                 id_user: str | uuid.UUID | None = None,
                 username: str | None = None
                 ):
        self.request = request
        self.log = log
        self.id_user = id_user
        self.username = username


async def get_handler(request: Request) -> Handler:
    token_data = {}
    if request.headers.get("Authorization", None):
        token_data = TokenUtils().decode_token(request=request)

    service_name = get_service_name(request=request)

    handler = Handler(request=request,
                      id_user=token_data.get("id_user", None),
                      log=logging.getLogger(service_name))

    return handler
