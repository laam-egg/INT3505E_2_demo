from ...db import copies_collection
from pymongo.collection import Collection
from .BaseCRUDService import BaseCRUDService

class CopyService(BaseCRUDService):
    def __init__(self, collection=None):
        # type: (CopyService, Collection|None) -> None
        collection = collection or copies_collection
        super().__init__(collection)
