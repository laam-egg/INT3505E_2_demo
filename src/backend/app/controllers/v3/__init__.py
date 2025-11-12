from flask import Blueprint
from flask_restx import Api, abort
from flask import jsonify
from flask_jwt_extended.exceptions import (
    NoAuthorizationError,
    InvalidHeaderError,
    JWTDecodeError,
    WrongTokenError,
    RevokedTokenError,
    UserClaimsVerificationError,
    FreshTokenRequired,
)
from werkzeug.exceptions import Forbidden

v3 = Blueprint("v3", __name__, url_prefix="/api/v3")

authorizations = {
    "Bearer": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": "Add 'Bearer <your_JWT_token>'"
    }
}

_api = Api(
    v3,
    title='Version 3',
    version='3',
    description='Add JWT authentication.',

    authorizations=authorizations,
)

from .patrons import patrons_api
from .titles import titles_api
from .copies import copies_api
from .borrows import borrows_api
from .users import users_api
from .auth import auth_api
from .payments import payments_api

_api.add_namespace(patrons_api)
_api.add_namespace(titles_api)
_api.add_namespace(copies_api)
_api.add_namespace(borrows_api)
_api.add_namespace(users_api)
_api.add_namespace(auth_api)
_api.add_namespace(payments_api)

@_api.errorhandler(NoAuthorizationError)
def handle_no_auth_error(e):
    return abort(401, "Missing Authorization header") # type: ignore

@_api.errorhandler(InvalidHeaderError)
def handle_invalid_header(e):
    return abort(422, "Invalid Authorization header") # type: ignore

@_api.errorhandler(JWTDecodeError)
def handle_invalid_token(e):
    return abort(401, "Invalid token") # type: ignore

@_api.errorhandler(WrongTokenError)
@_api.errorhandler(RevokedTokenError)
@_api.errorhandler(FreshTokenRequired)
@_api.errorhandler(UserClaimsVerificationError)
@_api.errorhandler(Forbidden)
def handle_bad_token(e):
    return abort(401, "Invalid token") # type: ignore
