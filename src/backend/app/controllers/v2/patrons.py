from flask import request, url_for
from flask_restx import Namespace, Resource, fields
from ...services.v1.PatronService import PatronService
from ...utils.pageable import Pageable
from ...utils.hateoas import HATEOAS
from flask_jwt_extended import jwt_required

#######################################
## STEP 1. DECLARE THE API NAMESPACE ##
#######################################

patrons_api = Namespace('patrons', 'Người sử dụng dịch vụ thư viện, e.g. mượn sách.')
api = patrons_api

####################################
## STEP 2. DEFINE THE MODELS/DTOs ##
####################################

patron_create_dto = api.model("PatronCreate", {
    "name": fields.String(required=True, description="Patron name", example="Vũ Tùng Lâm"),
})

patron_update_dto = api.model("PatronUpdate", {
    "name": fields.String(required=False, description="Patron name", example="Vũ Tùng Lâm"),
})

patron_replace_dto = api.clone("PatronReplace", patron_create_dto, {})

patron_dto = api.clone("Patron", patron_create_dto, {
    "id": fields.String(readonly=True, description="The patron ID"),
})

##################################
## STEP 3. CONNECT THE SERVICES ##
##################################

service = PatronService()

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
    


    @api.doc(description="Lấy danh sách tất cả các patrons, có pagination.", security="Bearer")
    @api.expect(get_collection_qp)
    @h.returns(
        patron_dto,
        as_list=True,
        self_links=lambda content: [],
        collection_links=lambda content: [url_for("v2.patrons_collection")],
    )
    @jwt_required()
    def get(self):
        args = self.get_collection_qp.parse_args()
        pageable = Pageable.from_query_params(args)
        return self.service.get_collection(pageable)
    


    @api.doc(description="Thêm patron mới.", security="Bearer")
    @api.expect(patron_create_dto)
    @h.returns(
        patron_dto,
        self_links=lambda content: [url_for("v2.patrons_item", patronId=content["id"])],
        collection_links=lambda content: [url_for("v2.patrons_collection")],
    )
    @jwt_required()
    def post(self):
        data = request.get_json()
        return self.service.post_item(data)




@api.route("/<string:patronId>")
class Item(Resource):
    service = service


    @api.doc(description="Lấy patron theo ID", security="Bearer")
    @h.returns(
        patron_dto,
        self_links=lambda content: [url_for("v2.patrons_item", patronId=content["id"])],
        collection_links=lambda content: [url_for("v2.patrons_collection")],
    )
    @jwt_required()
    def get(self, patronId):
        return self.service.get_item_by_id(patronId)


    
    @api.doc(description="Sửa toàn bộ patron, theo ID", security="Bearer")
    @api.expect(patron_replace_dto)
    @h.returns(
        patron_dto,
        self_links=lambda content: [url_for("v2.patrons_item", patronId=content["id"])],
        collection_links=lambda content: [url_for("v2.patrons_collection")],
    )
    @jwt_required()
    def put(self, patronId):
        data = request.get_json()
        return self.service.put_item_by_id(patronId, data)
    


    @api.doc(description="Sửa một phần patron, theo ID", security="Bearer")
    @api.expect(patron_update_dto)
    @h.returns(
        patron_dto,
        self_links=lambda content: [url_for("v2.patrons_item", patronId=content["id"])],
        collection_links=lambda content: [url_for("v2.patrons_collection")],
    )
    @jwt_required()
    def patch(self, patronId):
        data = request.get_json()
        return self.service.patch_item_by_id(patronId, data)





    @api.doc(description="Xóa patron, theo ID", security="Bearer")
    @h.returns(
        api.model("empty", {}),
        self_links=lambda content: [],
        collection_links=lambda content: [url_for("v2.patrons_collection")],
    )
    @jwt_required()
    def delete(self, patronId):
        self.service.delete_item_by_id(patronId)
        return {}
