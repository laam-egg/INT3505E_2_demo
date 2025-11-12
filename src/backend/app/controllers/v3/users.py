from flask import request, url_for
from flask_restx import Namespace, Resource, fields
from ...utils.pageable import Pageable
from ...utils.hateoas import HATEOAS
from flask_jwt_extended import jwt_required

#######################################
## STEP 1. DECLARE THE API NAMESPACE ##
#######################################

users_api = Namespace('users', 'Tài khoản người dùng hệ thống (quản trị viên, thủ thư...)')
api = users_api

####################################
## STEP 2. DEFINE THE MODELS/DTOs ##
####################################

user_create_dto = api.model("UserCreate", {
    "email": fields.String(required=True, description="Email"),
    "password": fields.String(required=True, description="Mật khẩu"),
    "fullName": fields.String(required=True, description="Họ tên đầy đủ"),
})

user_update_dto = api.model("UserUpdate", {
    "email": fields.String(required=False, description="Email mới"),
    "password": fields.String(required=False, description="Mật khẩu mới"),
    "fullName": fields.String(required=False, description="Họ tên đầy đủ mới"),
})

user_dto = api.clone("User", user_create_dto, {
    "id": fields.String(readonly=True, description="ID lượt mượn"),
})

##################################
## STEP 3. CONNECT THE SERVICES ##
##################################

from .services import user_service as service

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
            .add_argument('email', type=str, required=False, help='Email (optional)')
    )


    @api.doc(description="Lấy danh sách các users, có thể lọc theo email", security="Bearer")
    @h.returns(
        user_dto,
        as_list=True,
        self_links=lambda content: [],
        collection_links=lambda content: [url_for("v3.users_collection")],
    )
    @jwt_required()
    def get(self):
        args = self.get_collection_qp.parse_args()
        pageable = Pageable.from_query_params(args)

        email = args.get("email")
        email = str(email) if email else None

        if email:
            if pageable.page == 0:
                try:
                    user = self.service.get_item_by_email(email)
                    return [user]
                except Exception as e:
                    print(f"Exception raised but ignored: {e}")
                    return []
            else:
                return []
        else:
            return self.service.get_collection(pageable)
    


    @api.doc(description="Thêm user mới (đăng ký tài khoản).")
    @api.expect(user_create_dto)
    @h.returns(
        user_dto,
        self_links=lambda content: [url_for("v3.users_item", userId=content["id"])],
        collection_links=lambda content: [url_for("v3.users_collection")],
    )
    def post(self):
        data = request.get_json()
        return self.service.post_item(data)




@api.route("/<string:userId>")
class Item(Resource):
    service = service


    @api.doc(description="Lấy user theo ID", security="Bearer")
    @h.returns(
        user_dto,
        self_links=lambda content: [url_for("v3.users_item", userId=content["id"])],
        collection_links=lambda content: [url_for("v3.users_collection")],
    )
    @jwt_required()
    def get(self, userId):
        return self.service.get_item_by_id(userId)

    


    @api.doc(description="Sửa một phần user, theo ID", security="Bearer")
    @api.expect(user_update_dto)
    @h.returns(
        user_dto,
        self_links=lambda content: [url_for("v3.users_item", userId=content["id"])],
        collection_links=lambda content: [url_for("v3.users_collection")],
    )
    @jwt_required()
    def patch(self, userId):
        data = request.get_json()
        return self.service.patch_item_by_id(userId, data)





    @api.doc(description="Xóa user, theo ID", security="Bearer")
    @h.returns(
        api.model("empty", {}),
        self_links=lambda content: [],
        collection_links=lambda content: [url_for("v3.users_collection")],
    )
    @jwt_required()
    def delete(self, userId):
        self.service.delete_item_by_id(userId)
        return {}
