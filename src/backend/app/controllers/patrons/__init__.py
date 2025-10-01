from ..common import Controller
from .dto.patron import patron_dto

patrons_controller = Controller("patrons", __name__)

Patron = patron_dto(patrons_controller)

@patrons_controller.route('/')
class PatronList(patrons_controller.Resource):
    @patrons_controller.doc("Get all patrons")
    def get(self):
        return "<p>demo GET /api/v1/patrons</p>"

@patrons_controller.route('/<int:id>')
class PatronItem(patrons_controller.Resource):
    @patrons_controller.doc("Get patron by ID")
    @patrons_controller.marshal_with(Patron, code=200)
    def get(self, id):
        return { "patronId": id, "thisShouldBeFilteredOut": 123456 }
