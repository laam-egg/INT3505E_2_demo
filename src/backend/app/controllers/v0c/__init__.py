from flask import Blueprint
from flask_restx import Api
from ...utils.log import log

v0c = Blueprint("v0c", __name__, url_prefix="/api/v0c")

_api = Api(
    v0c,
    title='Sample API version (c)',
    version='0c',
    description='YET ANOTHER sample API version. Primarily created for Week 10 assignment purpose only.',
)

from .flaky import flaky_api

_api.add_namespace(flaky_api)
