from flask import request, url_for
from flask_restx import Namespace, Resource, fields
from ...utils.pageable import Pageable
from ...utils.hateoas import HATEOAS

#######################################
## STEP 1. DECLARE THE API NAMESPACE ##
#######################################

webhooks_api = Namespace('webhooks', 'Nhóm API có nghiệp vụ quản lý các subscriptions/webhooks.')
api = webhooks_api

####################################
## STEP 2. DEFINE THE MODELS/DTOs ##
####################################

webhook_create_dto = api.model("WebhookCreate", {
    "eventName": fields.String(required=True, description="Tên event cần subscribe", example="auth.login"),
    "targetUrl": fields.String(
        required=True, description=(
            "URL đích để gửi event (bằng cách POST với JSON payload gồm eventName và eventContent). "
            "Trong trường hợp webhook này được yêu cầu xóa, URL này sẽ được gọi với eventName = `webhook.deleted`,",
            "và response phải có status code là 2xx. Nếu không webhook sẽ KHÔNG được xóa."
        ),
        example="http://localhost:5001/webhook-destination",
    ),
})

webhook_dto = api.clone("Webhook", webhook_create_dto, {
    "id": fields.String(readonly=True, description="ID của webhook"),
})

##################################
## STEP 3. CONNECT THE SERVICES ##
##################################

from .services import webhook_service as service

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
            .add_argument('targetUrl', type=str, required=False, help='URL đích của webhook để filter')
    )

    


    @api.doc(description="Lấy danh sách các webhooks, có pagination.")
    @api.expect(get_collection_qp)
    @h.returns(
        webhook_dto,
        as_list=True,
        self_links=lambda content: [],
        collection_links=lambda content: [url_for("v4.webhooks_collection")],
    )
    def get(self):
        args = self.get_collection_qp.parse_args()
        pageable = Pageable.from_query_params(args)

        targetUrl = args.get("targetUrl")
        targetUrl = str(targetUrl) if targetUrl else None

        return self.service.get_collection_by_targetUrl(targetUrl, pageable)
    


    @api.doc(description="Thêm webhook mới.")
    @api.expect(webhook_create_dto)
    @h.returns(
        webhook_dto,
        self_links=lambda content: [url_for("v4.webhooks_item", webhookId=content["id"])],
        collection_links=lambda content: [url_for("v4.webhooks_collection")],
    )
    def post(self):
        data = request.get_json()
        return self.service.post_item(data)




@api.route("/<string:webhookId>")
class Item(Resource):
    service = service


    @api.doc(description="Lấy thông tin webhook theo ID")
    @h.returns(
        webhook_dto,
        self_links=lambda content: [url_for("v4.webhooks_item", webhookId=content["id"])],
        collection_links=lambda content: [url_for("v4.webhooks_collection")],
    )
    def get(self, webhookId):
        return self.service.get_item_by_id(webhookId)


    
    @api.doc(description="Xóa webhook, theo ID", security="Bearer")
    @h.returns(
        api.model("any", {
            "message": fields.String(description="Kết quả của thao tác xóa"),
        }),
        self_links=lambda content: [],
        collection_links=lambda content: [url_for("v4.webhooks_collection")],
    )
    def delete(self, webhookId):
        return self.service.delete_item_by_id(webhookId)
