from flask import Flask, url_for

app = Flask(__name__)

with app.app_context():
    from .controllers import register_api_controllers
    register_api_controllers(app)

    @app.get('/')
    def home():
        return f"""
        <html><head><title>Library Management System - Backend</title></head><body>
        <h1>Welcome to the Library Management System backend server!</h1>
        <a href={url_for("get_api_versions")}>Here is the API documentation.</a>
        </body></html>
        """

print(app.url_map)

if __name__ == '__main__':
    app.run(debug=True)
