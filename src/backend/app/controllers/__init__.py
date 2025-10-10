from .common import Controller
from flask import Flask, Blueprint
from flask_restx import Api

from .v1 import v1_controller
from .v2 import v2_controller

VERSIONS = {
    "v1": v1_controller,
    "v2": v2_controller,
}

def register_all(app):
    # type: (Flask) -> Flask
    for version, subcontroller in VERSIONS.items():
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

        api_blueprint = subcontroller.bind(api_blueprint, api)

        app.register_blueprint(api_blueprint)
    
    return app
