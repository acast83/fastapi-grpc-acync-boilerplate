from core.repository import BaseRepository
from ..models import Lookups


class LookupsRepository(BaseRepository[Lookups]):
    """
    Lookups repository provides all the database operations for the Lookups model.
    """
    db_name = None
