from ...db import borrows_collection
from pymongo.collection import Collection
from .BaseCRUDService import BaseCRUDService
from ...utils.pageable import Pageable
from pymongo import ASCENDING, DESCENDING
from typing import Any, override
from datetime import datetime

class BorrowService(BaseCRUDService):
    def __init__(self, collection=None):
        # type: (BorrowService, Collection|None) -> None
        collection = collection or borrows_collection
        super().__init__(collection)
    
    def get_collection_by_patronId_and_copyId_orderBy_statusLastUpdatedAt_DESC(
        self, patronId: str | None, copyId: str | None, pageable: Pageable
    ):
        """
        Tìm và trả về danh sách các lượt mượn theo patronId và copyId,
        có pagination. Gần nhất trước.

        Nếu một trường (patronId hoặc copyId) là None
        thì không lookup theo trường đó.
        """
        q = {}
        if patronId:
            q['patronId'] = patronId
        if copyId:
            q['copyId'] = copyId
        
        return [
            *self.collection.find(
                q,
                sort=[('statusLastUpdatedAt', DESCENDING)],
                **pageable.get_kwargs()
            )
        ]
    
    @override
    def post_item(self, item_doc):
        now = datetime.now()
        item_doc = {
            **item_doc,
            "status": "BORROWING",
            "createdAt": now,
            "statusLastUpdatedAt": now,
        }
        return super().post_item(item_doc)
    
    @override
    def put_item_by_id(self, id, item_doc):
        now = datetime.now()
        item_doc = {
            **item_doc,
            "statusLastUpdatedAt": now,
        }
        return super().put_item_by_id(id, item_doc)
    
    @override
    def patch_item_by_id(self, id, item_patch_doc):
        now = datetime.now()
        item_patch_doc = {
            **item_patch_doc,
            "statusLastUpdatedAt": now,
        }
        return super().patch_item_by_id(id, item_patch_doc)
