from flask import request, url_for
from flask_restx import Namespace, Resource, fields
from ...services.v2.PaymentService import PaymentStatus
from ...utils.pageable import Pageable
from ...utils.hateoas import HATEOAS
from flask_jwt_extended import jwt_required

#######################################
## STEP 1. DECLARE THE API NAMESPACE ##
#######################################

payments_api = Namespace('payments', 'Biểu diễn một giao dịch thanh toán của patron đối với thư viện.')
api = payments_api

####################################
## STEP 2. DEFINE THE MODELS/DTOs ##
####################################

payment_create_dto = api.model("PaymentCreate", {
    "patronId": fields.String(required=True, description="Patron ID"),
    "amount": fields.Float(required=True, description="Lượng tiền giao dịch"),
    "currency": fields.String(required=True, description="Đồng tiền giao dịch ; viết không dấu", example="VND"),
    "status": fields.String(required=False, default=PaymentStatus.UNVERIFIED, description="Trạng thái giao dịch ; nhận một trong các giá trị: " + ', '.join(PaymentStatus.POSSIBLE_VALUES)),
})

payment_update_dto = api.model("PaymentUpdate", {
    "status": fields.String(required=False, description="Trạng thái giao dịch ; nhận một trong các giá trị: " + ', '.join(PaymentStatus.POSSIBLE_VALUES)),
})

payment_dto = api.clone("Payment", payment_create_dto, {
    "id": fields.String(readonly=True, description="The payment ID"),
})

##################################
## STEP 3. CONNECT THE SERVICES ##
##################################

from .services import payment_service as service

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
        Pageable.pageable_query_params()
            .add_argument('patronId', type=str, required=False, help='Patron ID (optional)')
            .add_argument('status', type=str, required=False, help='Trạng thái của payment, nhận một trong các giá trị: ' + ", ".join(PaymentStatus.POSSIBLE_VALUES))
    )
    


    @api.doc(description="Lấy danh sách tất cả các payments, có pagination.", security="Bearer")
    @api.expect(get_collection_qp)
    @h.returns(
        payment_dto,
        as_list=True,
        self_links=lambda content: [],
        collection_links=lambda content: [url_for("v4.payments_collection")],
    )
    @jwt_required()
    def get(self):
        args = self.get_collection_qp.parse_args()
        pageable = Pageable.from_query_params(args)
        patronId = args.get("patronId") or None
        status = args.get("status") or None
        return self.service.get_collection_by_patronId_and_status_orderBy_createdAt_DESC(
            patronId=patronId,
            status=status,
            pageable=pageable,
        )
    


    @api.doc(description="Thêm payment mới.", security="Bearer")
    @api.expect(payment_create_dto)
    @h.returns(
        payment_dto,
        self_links=lambda content: [url_for("v4.payments_item", paymentId=content["id"])],
        collection_links=lambda content: [url_for("v4.payments_collection")],
    )
    @jwt_required()
    def post(self):
        data = request.get_json()
        return self.service.post_item(data)




@api.route("/<string:paymentId>")
class Item(Resource):
    service = service


    @api.doc(description="Lấy payment theo ID", security="Bearer")
    @h.returns(
        payment_dto,
        self_links=lambda content: [url_for("v4.payments_item", paymentId=content["id"])],
        collection_links=lambda content: [url_for("v4.payments_collection")],
    )
    @jwt_required()
    def get(self, paymentId):
        return self.service.get_item_by_id(paymentId)


    
    @api.doc(description="Sửa một phần payment, theo ID", security="Bearer")
    @api.expect(payment_update_dto)
    @h.returns(
        payment_dto,
        self_links=lambda content: [url_for("v4.payments_item", paymentId=content["id"])],
        collection_links=lambda content: [url_for("v4.payments_collection")],
    )
    @jwt_required()
    def patch(self, paymentId):
        data = request.get_json()
        return self.service.patch_item_by_id(paymentId, data)





    @api.doc(description="Xóa payment, theo ID", security="Bearer")
    @h.returns(
        api.model("empty", {}),
        self_links=lambda content: [],
        collection_links=lambda content: [url_for("v4.payments_collection")],
    )
    @jwt_required()
    def delete(self, paymentId):
        self.service.delete_item_by_id(paymentId)
        return {}
