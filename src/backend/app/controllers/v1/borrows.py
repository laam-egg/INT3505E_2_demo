from flask import request, url_for
from flask_restx import Namespace, Resource, fields
from ...services.v1.BorrowService import BorrowService
from ...utils.pageable import Pageable
from ...utils.hateoas import HATEOAS

#######################################
## STEP 1. DECLARE THE API NAMESPACE ##
#######################################

borrows_api = Namespace('borrows', 'Biểu diễn một lượt mượn sách từ thư viện.')
api = borrows_api

####################################
## STEP 2. DEFINE THE MODELS/DTOs ##
####################################

borrow_create_dto = api.model("BorrowCreate", {
    "patronId": fields.String(required=True, description="ID người mượn (patron)"),
    "copyId": fields.String(required=True, description="ID bản sao của một sách nào đó được mượn"),
})

borrow_update_dto = api.model("BorrowUpdate", {
    "status": fields.String(required=False, description="Trạng thái mới của lượt mượn: BORROWING, RETURNED, or LOST"),
})

# Lượt mượn không được phép sửa (patch) hoặc replace (put)
# bất kỳ thông tin nào khác status.

borrow_dto = api.clone("Borrow", borrow_create_dto, {
    "id": fields.String(readonly=True, description="ID lượt mượn"),
    "status": fields.String(required=True, description="Trạng thái của lượt mượn: BORROWING, RETURNED, or LOST"),
    "createdAt": fields.String(readonly=True, description="Thời gian mượn (tức thời gian tạo lượt mượn)"),
    "statusLastUpdatedAt": fields.String(readonly=True, description="Thời gian cuối cùng trạng thái của lượt mượn này được cập nhật"),
})

##################################
## STEP 3. CONNECT THE SERVICES ##
##################################

service = BorrowService()

###################################
## STEP 4. DEFINE THE CONTROLLER ##
## using the namespace, DTOs and ##
## services we have just defined ##
###################################

h = HATEOAS(api)

@api.route("/")
class Collection(Resource):
    service = service

    get_collection_qp = (
        Pageable
            .pageable_query_params()
            .add_argument('patronId', type=str, required=False, help='Patron ID (optional)')
            .add_argument('copyId', type=str, required=False, help="Copy ID (optional)")
    )
    


    @api.doc(description="Lấy danh sách tất cả các borrows, có pagination. Có thể lọc theo patronId.")
    @api.expect(get_collection_qp)
    @h.returns(
        borrow_dto,
        as_list=True,
        self_links=lambda content: [],
        collection_links=lambda content: [url_for("v1.borrows_collection")],
    )
    def get(self):
        args = self.get_collection_qp.parse_args()
        pageable = Pageable.from_query_params(args)

        patronId = args.get("patronId")
        patronId = str(patronId) if patronId else None

        copyId = args.get("copyId")
        copyId = str(copyId) if copyId else None

        return self.service.get_collection_by_patronId_and_copyId_orderBy_statusLastUpdatedAt_DESC(
            patronId,
            copyId,
            pageable,
        )
    


    @api.doc(description="Thêm borrow mới.")
    @api.expect(borrow_create_dto)
    @h.returns(
        borrow_dto,
        self_links=lambda content: [url_for("v1.borrows_item", borrowId=content["id"])],
        collection_links=lambda content: [url_for("v1.borrows_collection")],
    )
    def post(self):
        data = request.get_json()
        return self.service.post_item(data)




@api.route("/<string:borrowId>")
class Item(Resource):
    service = service


    @api.doc(description="Lấy borrow theo ID")
    @h.returns(
        borrow_dto,
        self_links=lambda content: [url_for("v1.borrows_item", borrowId=content["id"])],
        collection_links=lambda content: [url_for("v1.borrows_collection")],
    )
    def get(self, borrowId):
        return self.service.get_item_by_id(borrowId)

    


    @api.doc(description="Sửa một phần borrow, theo ID")
    @api.expect(borrow_update_dto)
    @h.returns(
        borrow_dto,
        self_links=lambda content: [url_for("v1.borrows_item", borrowId=content["id"])],
        collection_links=lambda content: [url_for("v1.borrows_collection")],
    )
    def patch(self, borrowId):
        data = request.get_json()
        return self.service.patch_item_by_id(borrowId, data)





    @api.doc(description="Xóa borrow, theo ID")
    @h.returns(
        api.model("empty", {}),
        self_links=lambda content: [],
        collection_links=lambda content: [url_for("v1.borrows_collection")],
    )
    def delete(self, borrowId):
        self.service.delete_item_by_id(borrowId)
        return {}
