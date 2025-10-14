from ...db import titles_collection
from pymongo.collection import Collection
from .BaseCRUDService import BaseCRUDService
from .CopyService import CopyService
from ...utils.pageable import Pageable
from typing import Any, override

class TitleService(BaseCRUDService):
    def __init__(self, collection=None, copy_service=None):
        # type: (TitleService, Collection|None, CopyService|None) -> None
        collection = collection or titles_collection
        super().__init__(collection)
        if copy_service is None:
            copy_service = CopyService()

        self.copy_service = copy_service
    
    @override
    def get_collection(self, pageable: Pageable) -> Any:
        return self.add_stats(
            super().get_collection(pageable)
        )
    
    @override
    def get_item_by_id(self, id):
        return self.add_stats(
            super().get_item_by_id(id)
        )
    
    @override
    def post_item(self, item_doc):
        return self.add_stats(
            super().post_item(item_doc)
        )
    
    @override
    def put_item_by_id(self, id, item_doc):
        return self.add_stats(
            super().put_item_by_id(id, item_doc)
        )
    
    @override
    def patch_item_by_id(self, id, item_patch_doc):
        return self.add_stats(
            super().patch_item_by_id(id, item_patch_doc)
        )
    
    def add_stats(self, doc):
        if isinstance(doc, list):
            return [*map(self.add_stats, doc)]
        
        docId = str(doc.get('id', doc.get('_id', None)))
        if not docId:
            raise RuntimeError("no id in doc", doc)
        
        return {
            **doc,
            **self.compute_title_stats(docId)
        }

    def compute_title_stats(self, titleId: str):
        pageable = Pageable(0, 20)

        total_copies = 0
        available_count = 0
        borrowed_count = 0
        lost_count = 0

        while True:
            copies = self.copy_service.get_collection_by_titleId(titleId, pageable)
            n = len(copies)
            if n == 0: break
            total_copies += n

            for copy in copies:
                copyId = str(copy["_id"])
                status = self.copy_service.get_item_status_by_id(copyId)
                if status == "AVAILABLE":
                    available_count += 1
                elif status == "BORROWED":
                    borrowed_count += 1
                elif status == "LOST":
                    lost_count += 1
        
        return {
            "totalCopies": total_copies,
            "availableCopies": available_count,
            "borrowedCopies": borrowed_count,
            "lostCopies": lost_count
        }
