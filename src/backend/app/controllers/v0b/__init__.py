from flask import Blueprint
from flask_restx import Api

v0b = Blueprint("v0b", __name__, url_prefix="/api/v0b")

_api = Api(
    v0b,
    title='Sample API version (b)',
    version='0b',
    description='ANOTHER sample API version for everyone in the group to understand the architecture. STILL, it does not satisfy even one actual business requirement.',
)

from .books import books_api
from .authors import authors_api

_api.add_namespace(books_api)
_api.add_namespace(authors_api)
