from flask import request, url_for
from flask_restx import Namespace, Resource, fields
from ...services.SampleBookService import SampleBookService
from ...utils.pageable import Pageable
from ...utils.hateoas import HATEOAS

#######################################
## STEP 1. DECLARE THE API NAMESPACE ##
#######################################

books_api = Namespace('books', 'Description of the resource, e.g. this represents book resource.')

####################################
## STEP 2. DEFINE THE MODELS/DTOs ##
####################################

book_create_dto = books_api.model("BookCreate", {
    "title": fields.String(required=True, description="The book title", example="Principles of Web API Design - Delivering Value with APIs and Microservices"),
    "isbn": fields.String(required=True, description="The book ISBN (International Standard Book Number)", example="978-0-13-735563-1"),
    "edition": fields.Integer(required=True, description="Edition number", example=1),
    "authors": fields.String(required=True, description="Newline-separated list of authors", example="James Higginbotham"),
    "yearOfPublication": fields.Integer(required=True, description="Year of publication", example=2022),
    "tags": fields.String(required=True, description="Newline-separated list of tags", example="Web\nAPI\nProgramming\nMicroservices"),
})

book_dto = books_api.clone("Book", book_create_dto, {
    "id": fields.String(readonly=True, description="The book ID"),
})

##################################
## STEP 3. CONNECT THE SERVICES ##
##################################

book_service = SampleBookService()

###################################
## STEP 4. DEFINE THE CONTROLLER ##
## using the namespace, DTOs and ##
## services we have just defined ##
###################################

h = HATEOAS(books_api)

@books_api.route("/")
class Collection(Resource):
    book_service = book_service

    # query params for the get-books api
    get_books_qp = Pageable.pageable_query_params()
    


    @books_api.doc("Lấy tất cả các đầu sách, có pagination.")
    @books_api.expect(get_books_qp)
    @h.returns(
        book_dto,
        as_list=True,
        self_links=lambda content: [],
        collection_links=lambda content: [url_for("v0b.books_collection")],
    )
    def get(self):
        args = self.get_books_qp.parse_args()
        pageable = Pageable.from_query_params(args)
        return self.book_service.get_books(pageable)
    


    @books_api.doc("Thêm đầu sách mới.")
    @books_api.expect(book_create_dto)
    @h.returns(
        book_dto,
        self_links=lambda content: [url_for("v0b.books_item", bookId=content["id"])],
        collection_links=lambda content: [],
    )
    def post(self):
        data = request.get_json()
        return self.book_service.create_book(data)




@books_api.route("/<string:bookId>")
class Item(Resource):
    book_service = book_service


    @books_api.doc("Lấy đầu sách theo ID")
    @h.returns(
        book_dto,
        self_links=lambda content: [url_for("v0b.books_item", bookId=content["id"])],
        collection_links=lambda content: [url_for("v0b.books_collection")],
    )
    def get(self, bookId):
        return self.book_service.get_book_by_id(bookId)
