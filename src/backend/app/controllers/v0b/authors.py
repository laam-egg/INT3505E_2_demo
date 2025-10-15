from flask_restx import Namespace, Resource

authors_api = Namespace('authors', 'This represents book authors.')

@authors_api.route("/")
class Author(Resource):
    def get(self):
        return {}
