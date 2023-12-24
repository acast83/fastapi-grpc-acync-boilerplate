import uuid
from typing import Any, Generic, Type, TypeVar

from fastapi import HTTPException, status
from pydantic import BaseModel
from tortoise import Model

from core.handler.handler import Handler

ModelType = TypeVar("ModelType", bound=Model)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType]):
    """Base class for data repositories."""

    def __init__(self, model: Type[ModelType],
                 # handler: Handler
                 ):
        self.model_class: Type[ModelType] = model
        # self.handler: Handler = handler

    async def create_in_db(self, attributes: dict[str, Any] = None) -> ModelType:
        """
        Creates the model instance.

        :param attributes: The attributes to create the model with.
        :return: The created model instance.
        """

        if attributes is None:
            attributes = {}
        model = self.model_class(**attributes)
        await model.save()
        return model

    async def get_all(self, query_params: dict = None, prefetched: list[str] = None,
                      order_by: str = None
                      ) -> list[ModelType]:
        """
        Returns a list of model instances.

        :param query_params: parameters used for query.
        :param prefetched: list of connected tables for prefetch.
        :param order_by: order by database records

        :return: A list of model instances.
        """
        if query_params:
            query = self.model_class.filter(**query_params)
        else:
            query = self.model_class.all()
        if prefetched:
            query = query.prefetch_related(*prefetched)
        if order_by:
            query = query.order_by(order_by)
        return await query

    async def get_single_by_params(
            self,
            query_params: dict,
            prefetched: list | None = None,
            raise_error: bool = True

    ) -> ModelType:
        """
        Returns the model instance matching the field and value.

        :param query_params: parameters used for query.
        :param prefetched: list of connected tables for prefetch.
        :param raise_error: if True returns an error in case of missing db record

        :return: The model instance.
        """
        query = self.model_class.filter(**query_params)
        if prefetched:
            query = query.prefetch_related(*prefetched)
        query = query.get_or_none()
        try:
            db_item = await query
        except Exception as e:
            raise
        if raise_error and not db_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"{self.model_class.__name__}_NOT_FOUND")
        return db_item

    async def delete(self, db_item_id: uuid.UUID) -> None:
        """
        Deletes the model.

        :param db_item_id: id of the database record.
        :return: None
        """

        db_item = await self.model_class.filter(id=db_item_id, active=True).get_or_none()
        if not db_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"{self.model_class.__name__}_NOT_FOUND")
        db_item.active = None
        await db_item.save()
