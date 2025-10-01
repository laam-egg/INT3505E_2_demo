from ..common import Controller

titles_controller = Controller("titles", __name__)

@titles_controller.route('/')
class TitleList(titles_controller.Resource):
    @titles_controller.doc("Get all titles")
    def get(self):
        return "<p>demo GET /api/v1/titles</p>"
    
@titles_controller.route("/<int:id>")
class TitleItem(titles_controller.Resource):
    @titles_controller.doc('Get title by ID')
    def get(self, id):
        return { "titleId": id }
