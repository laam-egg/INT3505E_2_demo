from ...db import copies_collection
from pymongo.collection import Collection
from .BaseCRUDService import BaseCRUDService

class BorrowService(BaseCRUDService):
    def __init__(self, collection=None):
        # type: (BorrowService, Collection|None) -> None
        collection = collection or copies_collection
        super().__init__(collection)
