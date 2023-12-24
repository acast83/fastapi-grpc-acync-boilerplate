from core.repository import BaseRepository
from ..models import Message


class ActivityLogRepository(BaseRepository[Message]):
    """
    User repository provides all the database operations for the User model.
    """
    db_name = None
