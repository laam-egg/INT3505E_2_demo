from ....common import Controller, fields

def patron_dto(controller):
    # type: (Controller) -> any
    return controller.dto("Patron", {
        "id": fields.String(readonly=True, description="The patron ID"),
        "name": fields.String(required=True, description="Patron name"),
    })

def patron_create_dto(controller):
    # type: (Controller) -> any
    return controller.dto("PatronCreate", {
        "name": fields.String(required=True, description="Patron name"),
    }, write=True)

def patron_update_dto(controller):
    # type: (Controller) -> any
    return controller.dto("PatronUpdate", {
        "name": fields.String(description="Patron name"),
    }, write=True)
