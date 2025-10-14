from ...db import patrons_collection
from pymongo.collection import Collection
from .BaseCRUDService import BaseCRUDService

class PatronService(BaseCRUDService):
    def __init__(self, collection=None):
        # type: (PatronService, Collection|None) -> None
        collection = collection or patrons_collection
        super().__init__(collection)
