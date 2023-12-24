from typing import Generic, Type, TypeVar

from tortoise import Model

from core.repository import BaseRepository

ModelType = TypeVar("ModelType", bound=Model)


class BaseService(Generic[ModelType]):
    """Base class for data service."""

    def __init__(self, repository: BaseRepository):
        self.repository = repository
