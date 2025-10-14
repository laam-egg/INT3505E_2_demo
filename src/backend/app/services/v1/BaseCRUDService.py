from ...db import str_to_objectid
from ...utils.pageable import Pageable
from typing import Any
from pymongo import ASCENDING, DESCENDING
from pymongo.collection import Collection
from flask_restx import abort

class BaseCRUDService:
    def __init__(self, collection):
        # type: (BaseCRUDService, Collection) -> None
        self.collection = collection

    def get_collection(self, pageable):
        # type: (BaseCRUDService, Pageable) -> Any
        """
        Trả về danh sách tất cả bản ghi, theo pagination.
        """
        return [
            *self.collection.find(
                skip=pageable.get_skip(),
                limit=pageable.get_limit(),
                sort=[('_id', ASCENDING)],
            )
        ]
    
    def post_item(self, item_doc):
        """
        Tạo bản ghi mới. Trả về nội dung bản ghi vừa tạo, trong đó có ID.
        """
        result = self.collection.insert_one(item_doc)
        return {
            "_id": result.inserted_id,
            **item_doc
        }
    
    def get_item_by_id(self, id):
        """
        Tìm và trả về bản ghi theo ID. Nếu không có, throw 404.
        """
        object_id = str_to_objectid(id)
        if not object_id:
            abort(404, "Invalid ID") # type: ignore
        result = self.collection.find_one({ "_id": object_id })
        if not result:
            abort(404, "Item not found") # type: ignore
        return result
    
    def put_item_by_id(self, id, item_doc):
        """
        Sửa toàn bộ bản ghi theo ID. Nếu không có, throw 404.
        Trả về bản ghi đã sửa.
        """
        object_id = str_to_objectid(id)
        if not object_id:
            abort(404, "Invalid ID") # type: ignore
        item_doc = {
            **item_doc,
            "_id": object_id,
        }
        result = self.collection.find_one_and_replace(
            { "_id": object_id },
            item_doc,
            return_document=True
        )

        if not result:
            abort(404, "Item not found") # type: ignore
        
        return result
    
    def patch_item_by_id(self, id, item_patch_doc):
        """
        Sửa một phần bản ghi theo ID. Nếu không có, throw 404.
        Trả về bản ghi đã sửa.
        """
        object_id = str_to_objectid(id)
        if not object_id:
            abort(404, "Invalid ID") # type: ignore
        result = self.collection.find_one_and_update(
            { "_id": object_id },
            { '$set': item_patch_doc },
            return_document=True
        )

        if not result:
            abort(404, "Item not found") # type: ignore
        
        return result
    
    def delete_item_by_id(self, id):
        """
        Xóa bản ghi theo ID. Nếu không có, throw 404.
        Trả về None.
        """
        object_id = str_to_objectid(id)
        if not object_id:
            abort(404, "Invalid ID") # type: ignore
        
        result = self.collection.delete_one({
            "_id": object_id,
        })

        if result.deleted_count == 0:
            abort(404, "Item not found") # type: ignore
