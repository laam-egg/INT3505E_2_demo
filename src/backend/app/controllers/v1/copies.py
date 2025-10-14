from flask import request, url_for
from flask_restx import Namespace, Resource, fields
from ...services.v1.CopyService import CopyService
from ...utils.pageable import Pageable
from ...utils.hateoas import HATEOAS

#######################################
## STEP 1. DECLARE THE API NAMESPACE ##
#######################################

copies_api = Namespace(
    'copies', 'Nhóm API có nghiệp vụ quản lý các bản sao (copies) của các đầu sách (titles).',
    path="/titles/<string:titleId>/copies"
)
api = copies_api

####################################
## STEP 2. DEFINE THE MODELS/DTOs ##
####################################

copy_create_dto = api.model("CopyCreate", {
    "code": fields.String(required=True, description="Code/identifier của bản sao"),
})

copy_update_dto = api.model("CopyUpdate", {
    "code": fields.String(required=False, description="Code/identifier của bản sao"),
})

copy_replace_dto = api.clone("CopyReplace", copy_create_dto, {})

copy_dto = api.clone("Copy", copy_create_dto, {
    "id": fields.String(readonly=True, description="ID của bản sao"),
    "titleId": fields.String(required=True, description="ID của đầu sách tương ứng"),
    "status": fields.String(readonly=True, description="Trạng thái hiện tại của bản sao: AVAILABLE, BORROWED, or LOST"),
})

##################################
## STEP 3. CONNECT THE SERVICES ##
##################################

service = CopyService()

###################################
## STEP 4. DEFINE THE CONTROLLER ##
## using the namespace, DTOs and ##
## services we have just defined ##
###################################

h = HATEOAS(api)

@api.route("/")
class Collection(Resource):
    service = service

    get_collection_qp = Pageable.pageable_query_params()
    


    @api.doc("Lấy danh sách tất cả các copies của một title, có pagination.")
    @api.expect(get_collection_qp)
    @h.returns(
        copy_dto,
        as_list=True,
        self_links=lambda content: [],
        collection_links=lambda content: [] if len(content) == 0 else [url_for( "v1.copies_collection", titleId=content[0]["titleId"])],
    )
    def get(self, titleId):
        args = self.get_collection_qp.parse_args()
        pageable = Pageable.from_query_params(args)
        return self.service.get_collection_by_titleId(titleId, pageable)
    


    @api.doc("Thêm bản sao mới cho một đầu sách.")
    @api.expect(copy_create_dto)
    @h.returns(
        copy_dto,
        self_links=lambda content: [url_for("v1.copies_item", titleId=content["titleId"], copyId=content["id"])],
        collection_links=lambda content: [url_for("v1.copies_collection", titleId=content["titleId"])],
    )
    def post(self, titleId):
        data = request.get_json()
        return self.service.post_item_with_titleId(titleId, data)




@api.route("/<string:copyId>")
class Item(Resource):
    service = service


    @api.doc("Lấy copy theo ID")
    @h.returns(
        copy_dto,
        self_links=lambda content: [url_for("v1.copies_item", titleId=content["titleId"], copyId=content["id"])],
        collection_links=lambda content: [url_for("v1.copies_collection", titleId=content["titleId"])],
    )
    def get(self, titleId, copyId):
        return self.service.get_item_by_id_and_titleId(titleId, copyId)


    
    @api.doc("Sửa toàn bộ copy, theo ID")
    @api.expect(copy_replace_dto)
    @h.returns(
        copy_dto,
        self_links=lambda content: [url_for("v1.copies_item", titleId=content["titleId"], copyId=content["id"])],
        collection_links=lambda content: [url_for("v1.copies_collection", titleId=content["titleId"])],
    )
    def put(self, titleId, copyId):
        data = request.get_json()
        return self.service.put_item_by_id_with_titleId(titleId, copyId, data)
    


    @api.doc("Sửa một phần copy, theo ID")
    @api.expect(copy_update_dto)
    @h.returns(
        copy_dto,
        self_links=lambda content: [url_for("v1.copies_item", titleId=content["titleId"], copyId=content["id"])],
        collection_links=lambda content: [url_for("v1.copies_collection", titleId=content["titleId"])],
    )
    def patch(self, titleId, copyId):
        data = request.get_json()
        return self.service.patch_item_by_id_with_titleId(titleId, copyId, data)
    



    @api.doc("Xóa copy, theo ID")
    @h.returns(
        api.model("empty", {}),
        self_links=lambda content: [],
        collection_links=lambda content: [url_for("v1.copies_collection", titleId=content["titleId"])],
    )
    def delete(self, titleId, copyId):
        self.service.delete_item_by_id_and_titleId(titleId, copyId)
        return {}
