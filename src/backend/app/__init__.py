from flask import Flask
from flask_restx import Api
from .controllers import api_controller

app = Flask(__name__)

api = Api(
    app,
    version="1.0",
    title="My API",
    description="A simple demo API",
    doc="/api/docs",
)

app = api_controller.bind(app, api)

@app.get("/api/json")
def swagger_oas_json():
    return api.__schema__
