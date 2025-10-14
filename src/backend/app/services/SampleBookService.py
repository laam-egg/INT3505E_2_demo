from ..db import str_to_objectid, test_books_collection_
from ..utils.pageable import Pageable
from typing import Any
from pymongo import ASCENDING, DESCENDING
from flask_restx import abort

class SampleBookService:
    def __init__(self, books_collection=test_books_collection_):
        self.books_collection = books_collection

    def get_books(self, pageable):
        # type: (SampleBookService, Pageable) -> Any
        """
        Lấy danh sách tất cả books, theo pagination.
        """
        return [
            *self.books_collection.find(
                skip=pageable.get_skip(),
                limit=pageable.get_limit(),
                sort=[('_id', ASCENDING)],
            )
        ]
    
    def create_book(self, book_doc):
        """
        Tạo book mới. Trả về nội dung book vừa tạo, trong đó có ID.
        """
        result = self.books_collection.insert_one(book_doc)
        return {
            "_id": result.inserted_id,
            **book_doc
        }
    
    def get_book_by_id(self, book_id):
        """
        Tìm và trả về book theo ID. Nếu không có, throw 404.
        """
        object_id = str_to_objectid(book_id)
        if not object_id:
            abort(404, "Invalid ID") # type: ignore
        result = self.books_collection.find_one({ "_id": object_id })
        if not result:
            abort(404, "Book not found") # type: ignore
        return result
