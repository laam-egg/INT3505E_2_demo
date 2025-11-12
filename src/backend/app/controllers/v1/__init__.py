from flask import Blueprint
from flask_restx import Api

v1 = Blueprint("v1", __name__, url_prefix="/api/v1")

_api = Api(
    v1,
    title='Version 1',
    version='1',
    description='The first stable version.\n\nWARNING: This API version has been deprecated and will be removed in the near future. Please migrate to API v3 - the latest stable version.',
)

from .patrons import patrons_api
from .titles import titles_api
from .copies import copies_api
from .borrows import borrows_api

_api.add_namespace(patrons_api)
_api.add_namespace(titles_api)
_api.add_namespace(copies_api)
_api.add_namespace(borrows_api)
