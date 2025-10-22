from flask import Flask, Blueprint, url_for
from .v0a import v0a
from .v0b import v0b
from .v1 import v1
from .v2 import v2

class ApiVersion:
    def __init__(self, name, blueprint):
        # type: (ApiVersion, str, Blueprint) -> None
        self.name = name
        self.blueprint = blueprint

API_VERSIONS = [
    ApiVersion("v0a", v0a),
    ApiVersion("v0b", v0b),
    ApiVersion("v1", v1),
    ApiVersion("v2", v2),
] # type: list[ApiVersion]
















def register_api_controllers(app):
    # type: (Flask) -> None
    for api_version in API_VERSIONS:
        app.register_blueprint(api_version.blueprint)
    
    def build_api_version_doc_link(api_version):
        # type: (ApiVersion) -> str
        swagger_url = url_for(f"{api_version.name}.doc")

        return f"""
        <li>
            <a href="{swagger_url}">Version {api_version.name}</a>
        </li>
        """

    @app.get('/api', strict_slashes=False)
    def get_api_versions():
        links = "".join(
            build_api_version_doc_link(api_version) for api_version in API_VERSIONS
        )
        return f"""
        <html><head><title>API Documentation</title></head><body>
        <h1>API Documentation</h1>
        <div>
            <p>Here are all versions of the API, along with their respective documentation.</p>

            <ul>{links}</ul>
        </div>
        </body></html>
        """
