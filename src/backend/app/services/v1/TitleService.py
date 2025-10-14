from ...db import titles_collection
from pymongo.collection import Collection
from .BaseCRUDService import BaseCRUDService

class TitleService(BaseCRUDService):
    def __init__(self, collection=None):
        # type: (TitleService, Collection|None) -> None
        collection = collection or titles_collection
        super().__init__(collection)
