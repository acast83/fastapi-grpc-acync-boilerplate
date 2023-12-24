from tortoise.transactions import in_transaction

from core.repository import BaseRepository
from ..models import User


class UserRepository(BaseRepository[User]):
    """
    User repository provides all the database operations for the User model.
    """
    db_name = None

    async def update_user_display_and_search(self, user: User) -> User:
        async with in_transaction(connection_name="users"):
            await self.update_display_name(user=user)
            await self.update_search_field(user=user)
            await user.refresh_from_db()
        return user

    @staticmethod
    async def update_display_name(user: User) -> None:
        user.display_name = f"{user.first_name} {user.last_name}"
        await user.save()

    @staticmethod
    async def update_search_field(user: User) -> None:
        fields = ("username", "first_name", "last_name", "phone_number", "email")
        search_field = " ".join([getattr(user, f) for f in fields if getattr(user, f) is not None])
        user.search_field = f" {search_field.lower()}"
        await user.save()
