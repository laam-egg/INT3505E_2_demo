from ...common import Controller, fields

def patron_dto(
    controller, # type: Controller
):
    return controller.dto("Patron", {
        "patronId": fields.Integer(readonly=True, description="The patron ID"),
    })
