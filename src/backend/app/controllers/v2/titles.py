from flask import request, url_for
from flask_restx import Namespace, Resource, fields
from ...services.v1.TitleService import TitleService
from ...utils.pageable import Pageable
from ...utils.hateoas import HATEOAS
from flask_jwt_extended import jwt_required

#######################################
## STEP 1. DECLARE THE API NAMESPACE ##
#######################################

titles_api = Namespace('titles', 'Nhóm API có nghiệp vụ quản lý đầu sách (titles).')
api = titles_api

####################################
## STEP 2. DEFINE THE MODELS/DTOs ##
####################################

title_create_dto = api.model("TitleCreate", {
    "name": fields.String(required=True, description="Tên đầu sách", example="Principles of Web API Design - Delivering Value with APIs and Microservices"),
    "edition": fields.Integer(required=True, description="Số thứ tự của lần tái bản", example=1),
    "authors": fields.String(required=True, description="Tên các tác giả, phân cách bằng newlines", example="James Higginbotham"),
    "yearOfPublication": fields.Integer(required=True, description="Năm xuất bản", example=2022),
    "tags": fields.String(required=True, description="Các thẻ/tags, phân cách bằng newlines", example="Web\nAPI\nProgramming\nMicroservices"),
})

title_update_dto = api.model("TitleUpdate", {
    "name": fields.String(required=False, description="Tên đầu sách", example="Principles of Web API Design - Delivering Value with APIs and Microservices"),
    "edition": fields.Integer(required=False, description="Số thứ tự của lần tái bản", example=1),
    "authors": fields.String(required=False, description="Tên các tác giả, phân cách bằng newlines", example="James Higginbotham"),
    "yearOfPublication": fields.Integer(required=False, description="Năm xuất bản", example=2022),
    "tags": fields.String(required=False, description="Các thẻ/tags, phân cách bằng newlines", example="Web\nAPI\nProgramming\nMicroservices"),
})

title_replace_dto = api.clone("TitleReplace", title_create_dto, {})

title_dto = api.clone("Title", title_create_dto, {
    "id": fields.String(readonly=True, description="ID của đầu sách"),

    "totalCopies": fields.Integer(readonly=True, description="Tổng số bản sao của đầu sách này", default=0),
    "availableCopies": fields.Integer(readonly=True, description="Số bản sao đang có sẵn (có thể mượn được)", default=0),
    "borrowedCopies": fields.Integer(readonly=True, description="Số bản sao đang được mượn", default=0),
    "lostCopies": fields.Integer(readonly=True, description="Số bản sao đã bị báo hỏng/mất", default=0),
})

##################################
## STEP 3. CONNECT THE SERVICES ##
##################################

service = TitleService()

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
    


    @api.doc(description="Lấy danh sách tất cả các titles, có pagination.")
    @api.expect(get_collection_qp)
    @h.returns(
        title_dto,
        as_list=True,
        self_links=lambda content: [],
        collection_links=lambda content: [url_for("v2.titles_collection")],
    )
    def get(self):
        args = self.get_collection_qp.parse_args()
        pageable = Pageable.from_query_params(args)
        return self.service.get_collection(pageable)
    


    @api.doc(description="Thêm đầu sách mới.", security="Bearer")
    @api.expect(title_create_dto)
    @h.returns(
        title_dto,
        self_links=lambda content: [url_for("v2.titles_item", titleId=content["id"])],
        collection_links=lambda content: [url_for("v2.titles_collection")],
    )
    @jwt_required()
    def post(self):
        data = request.get_json()
        return self.service.post_item(data)




@api.route("/<string:titleId>")
class Item(Resource):
    service = service


    @api.doc(description="Lấy title theo ID")
    @h.returns(
        title_dto,
        self_links=lambda content: [url_for("v2.titles_item", titleId=content["id"])],
        collection_links=lambda content: [url_for("v2.titles_collection")],
    )
    def get(self, titleId):
        return self.service.get_item_by_id(titleId)


    
    @api.doc(description="Sửa toàn bộ title, theo ID", security="Bearer")
    @api.expect(title_replace_dto)
    @h.returns(
        title_dto,
        self_links=lambda content: [url_for("v2.titles_item", titleId=content["id"])],
        collection_links=lambda content: [url_for("v2.titles_collection")],
    )
    @jwt_required()
    def put(self, titleId):
        data = request.get_json()
        return self.service.put_item_by_id(titleId, data)
    


    @api.doc(description="Sửa một phần title, theo ID", security="Bearer")
    @api.expect(title_update_dto)
    @h.returns(
        title_dto,
        self_links=lambda content: [url_for("v2.titles_item", titleId=content["id"])],
        collection_links=lambda content: [url_for("v2.titles_collection")],
    )
    @jwt_required()
    def patch(self, titleId):
        data = request.get_json()
        return self.service.patch_item_by_id(titleId, data)
    



    @api.doc(description="Xóa title, theo ID", security="Bearer")
    @h.returns(
        api.model("empty", {}),
        self_links=lambda content: [],
        collection_links=lambda content: [url_for("v2.titles_collection")],
    )
    @jwt_required()
    def delete(self, titleId):
        self.service.delete_item_by_id(titleId)
        return {}
