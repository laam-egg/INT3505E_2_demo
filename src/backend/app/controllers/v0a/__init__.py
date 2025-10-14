from flask import Blueprint
from flask_restx import Api

v0a = Blueprint("v0a", __name__, url_prefix="/api/v0a")

_api = Api(
    v0a,
    title='Sample API version',
    version='0a',
    description='A sample API version for everyone in the group to understand the architecture. It does not satisfy even one actual business requirement.',
)

from .books import books_api

_api.add_namespace(books_api)
