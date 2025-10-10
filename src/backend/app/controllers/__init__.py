from .common import Controller
from flask import Flask, Blueprint
from flask_restx import Api

from .v1 import register_v1_controller
from .v2 import register_v2_controller

VERSIONS = {
    "v1": register_v1_controller,
    "v2": register_v2_controller,
}

def register_all(app):
    # type: (Flask) -> Flask
    for version, register in VERSIONS.items():
        api_blueprint = Blueprint(
            f"api{version}",
            __name__,
        )

        api = Api(
            api_blueprint,
            version=version,
            title="My API",
            description="A simple demo API",
            doc=f"/api/{version}/docs",
            prefix=f"/api/{version}",
        )

        api_blueprint = register(api_blueprint, api)

        app.register_blueprint(api_blueprint)
    
    return app
