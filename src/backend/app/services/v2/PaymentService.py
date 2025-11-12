from pymongo.collection import Collection
from ..BaseCRUDService import BaseCRUDService
from ...utils.pageable import Pageable
from pymongo import ASCENDING, DESCENDING

class PaymentStatus:
    UNVERIFIED = "UNVERIFIED" # new
    VERIFIED = "VERIFIED" # reported by patrol, confirmed by librarian
    CANCELLED = "CANCELLED" # cancelled by patrol
    DISVERIFIED = "DISVERIFIED" # reported by patrol, disproved by librarian

    POSSIBLE_VALUES = [
        UNVERIFIED,
        VERIFIED,
        CANCELLED,
        DISVERIFIED,
    ]

class PaymentService(BaseCRUDService):
    def __init__(self, collection):
        # type: (PaymentService, Collection) -> None
        super().__init__(collection)
    
    def get_collection_by_patronId_and_status_orderBy_createdAt_DESC(
        self, patronId: str | None, status: str | None, pageable: Pageable
    ):
        """
        Tìm và trả về danh sách các payment theo patronId và status,
        có pagination. Gần nhất trước.

        Nếu patronId trống thì không lọc theo patronId nữa.
        """
        q = {}
        if patronId:
            q['patronId'] = patronId
        if status:
            q['status'] = status
        
        return [
            *self.collection.find(
                q,
                sort=[('updatedAt', DESCENDING)],
                **pageable.get_kwargs()
            )
        ]
