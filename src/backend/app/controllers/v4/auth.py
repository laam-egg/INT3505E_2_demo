from flask import request, url_for
from flask_restx import Namespace, Resource, fields
from ...utils.pageable import Pageable
from ...utils.hateoas import HATEOAS
from .users import user_dto

#######################################
## STEP 1. DECLARE THE API NAMESPACE ##
#######################################

auth_api = Namespace('auth', 'API liên quan đến đăng nhập, xác thực')
api = auth_api

####################################
## STEP 2. DEFINE THE MODELS/DTOs ##
####################################

auth_login_dto = api.model("AuthLogin", {
    "email": fields.String(required=True, description="Email"),
    "password": fields.String(required=True, description="Mật khẩu"),
})

auth_dto = api.model("Auth", {
    "user": fields.Nested(user_dto),
    "accessToken": fields.String(required=True, description="Access Token"),
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

@api.route("/login")
class Login(Resource):
    service = service



    @api.doc(description="Đăng nhập")
    @h.expect(auth_login_dto)
    @h.returns(
        auth_dto,
        self_links=lambda content: [url_for("v4.users_item", userId=content["user"]["id"])],
        collection_links=lambda content: [],
    )
    def post(self):
        data = request.get_json()
        return self.service.login(data['email'], data['password'])
