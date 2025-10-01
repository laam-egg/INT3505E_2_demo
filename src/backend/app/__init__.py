from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from .controllers import api_controller

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.get("/")
def home_page():
    return """
    <body>
        <h1>Have a good day!</h1>

        <div>
            <p>
                This website seems to be working properly.
            </p>
        </div>

        <div>
            <p>Next steps:</p>
            <div>
                <h2>API v1</h2>
                <ul>
                    <li><a href="/api/v1/docs">API Documentation and Playground (Swagger UI)</a></li>
                    <li><a href="/api/v1/json">OpenAPI Specification Document (OAS) in JSON</a></li>
                </ul>
            </div>
        </div>
    </body>
    """

api = Api(
    app,
    version="1.0",
    title="My API",
    description="A simple demo API",
    doc="/api/v1/docs"
)

app = api_controller.bind(app, api)

@app.get("/api/v1/json")
def swagger_oas_json():
    return api.__schema__

print(app.url_map)
