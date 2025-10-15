from flask_restx import Namespace, Resource

books_api = Namespace('books', 'Description of the resource, e.g. this represents book resource.')

@books_api.route("/")
class Book(Resource):
    def get(self):
        return {}
