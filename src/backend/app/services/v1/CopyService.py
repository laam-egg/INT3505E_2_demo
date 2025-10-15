from pymongo.collection import Collection
from .BaseCRUDService import BaseCRUDService
from .BorrowService import BorrowService
from ...utils.pageable import Pageable
from pymongo import ASCENDING, DESCENDING
from flask_restx import abort
from typing import Any, override

class CopyService(BaseCRUDService):
    def __init__(self, collection=None, borrow_service=None):
        # type: (CopyService, Collection|None, BorrowService|None) -> None
        if collection is None:
            from ...db import copies_collection
            collection = copies_collection
        super().__init__(collection)

        if borrow_service is None:
            borrow_service = BorrowService()
        self.borrow_service = borrow_service

    @override
    def get_collection(self, pageable: Pageable) -> Any:
        return self.add_status(
            super().get_collection(pageable)
        )
    
    @override
    def get_item_by_id(self, id):
        return self.add_status(
            super().get_item_by_id(id)
        )
    
    @override
    def post_item(self, item_doc):
        return self.add_status(
            super().post_item(item_doc)
        )
    
    @override
    def put_item_by_id(self, id, item_doc):
        return self.add_status(
            super().put_item_by_id(id, item_doc)
        )
    
    @override
    def patch_item_by_id(self, id, item_patch_doc):
        return self.add_status(
            super().patch_item_by_id(id, item_patch_doc)
        )
    
    def get_collection_by_titleId(self, titleId, pageable: Pageable):
        """Trả về danh sách các copy theo titleId, có pagination, sort theo ID."""
        return self.add_status(
            [
                *self.collection.find(
                    { "titleId": titleId },
                    **pageable.get_kwargs(),
                    sort=[('_id', ASCENDING)],
                )
            ]
        )
    
    def post_item_with_titleId(self, titleId, item_doc):
        item_doc["titleId"] = str(titleId)
        return self.post_item({
            **item_doc,
            "titleId": titleId,
        })
    
    def get_item_by_id_and_titleId(self, titleId, copyId):
        copy = self.get_item_by_id(copyId)
        assert type(copy) is dict
        if str(copy["titleId"]) != str(titleId):
            abort(404, "Item not found") # type: ignore
        return copy # no need to wrap self.add_status() here because self.get_item_by_id() already does
    
    def put_item_by_id_with_titleId(self, titleId, copyId, item_doc):
        self.get_item_by_id_and_titleId(titleId, copyId) # to assert existence
        return self.put_item_by_id(copyId, item_doc)
    
    def patch_item_by_id_with_titleId(self, titleId, copyId, item_doc):
        self.get_item_by_id_and_titleId(titleId, copyId) # to assert existence
        return self.patch_item_by_id(copyId, item_doc)
    
    def delete_item_by_id_and_titleId(self, titleId, copyId):
        self.get_item_by_id_and_titleId(titleId, copyId) # to assert existence
        return self.delete_item_by_id(copyId)




        
    def add_status(self, copy):
        if isinstance(copy, list):
            return [*map(self.add_status, copy)]
        
        copyId = str(copy.get("id", copy.get("_id", "")))
        if not copyId:
            raise RuntimeError("No ID in Copy document???", copy)
        
        return {
            **copy,
            "status": self.get_item_status_by_id(copyId),
        }

    def get_item_status_by_id(self, copyId):
        """Lấy trạng thái của copy dựa vào lượt mượn gần nhất."""
        pageable = Pageable(0, 1)
        copy_borrows = self.borrow_service.get_collection_by_patronId_and_copyId_orderBy_statusLastUpdatedAt_DESC(
            patronId=None,
            copyId=copyId,
            pageable=pageable,
        )
        if len(copy_borrows) == 0:
            return "AVAILABLE"
        
        latest_borrow = copy_borrows[0]

        if latest_borrow["status"] == "BORROWING":
            return "BORROWED"
        elif latest_borrow["status"] == "LOST":
            return "LOST"
        else:  # RETURNED
            return "AVAILABLE"
