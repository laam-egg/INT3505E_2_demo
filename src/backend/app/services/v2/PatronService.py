from ...db import patrons_collection
from pymongo.collection import Collection
from ..BaseCRUDService import BaseCRUDService
from typing import override, Any
from .PaymentService import PaymentService, PaymentStatus
from pymongo import ASCENDING, DESCENDING
from ...utils.pageable import Pageable

class PatronService(BaseCRUDService):
    def __init__(self, collection, payment_service):
        # type: (PatronService, Collection, PaymentService) -> None
        super().__init__(collection)
        self.payment_service = payment_service
    
    @override
    def get_collection(self, pageable):
        return self.add_new_fields(
            super().get_collection(pageable)
        )
    
    @override
    def get_item_by_id(self, id):
        return self.add_new_fields(
            super().get_item_by_id(id)
        )
    
    @override
    def post_item(self, item_doc):
        return self.add_new_fields(
            super().post_item(item_doc)
        )
    
    @override
    def put_item_by_id(self, id, item_doc):
        return self.add_new_fields(
            super().put_item_by_id(id, item_doc)
        )
    
    @override
    def patch_item_by_id(self, id, item_patch_doc):
        return self.add_new_fields(
            super().patch_item_by_id(id, item_patch_doc)
        )
        
    def add_new_fields(self, doc):
        if isinstance(doc, list):
            return [*map(self.add_new_fields, doc)]
        
        docId = str(doc.get('id', doc.get('_id', "")))
        if not docId:
            raise RuntimeError("no id in doc", doc)
        
        return {
            **doc,
            **self.compute_new_fields(docId),
        }
    
    def compute_new_fields(self, patronId: str):
        return {
            "isPremium": self.get_item_isPremium_by_id(patronId),
        }

    def get_item_isPremium_by_id(self, patronId: str):
        """Lấy trạng thái isPremium của patron dựa vào lần purchase gần nhất.
        Hiện tại, chỉ cần patron có ủng hộ thư viện (>=1 payment) thì
        được coi là premium member."""

        pageable = Pageable(0, 1)
        most_recent_verified_payments = self.payment_service.get_collection_by_patronId_and_status_orderBy_createdAt_DESC(
            patronId=patronId,
            status=PaymentStatus.VERIFIED,
            pageable=pageable,
        )
        if len(most_recent_verified_payments) == 0:
            return False
        
        return True
