from ...common import Controller, fields

def copy_dto(controller):
    # type: (Controller) -> any
    return controller.dto("Copy", {
        "id": fields.String(readonly=True, description="The copy ID"),
        "titleId": fields.String(required=True, description="The title ID this copy belongs to"),
        "code": fields.String(required=True, description="Copy code/identifier"),
        "status": fields.String(readonly=True, description="Current status: AVAILABLE, BORROWED, or LOST"),
    })

def copy_create_dto(controller):
    # type: (Controller) -> any
    return controller.dto("CopyCreate", {
        "code": fields.String(required=True, description="Copy code/identifier"),
    })

def copy_update_dto(controller):
    # type: (Controller) -> any
    return controller.dto("CopyUpdate", {
        "code": fields.String(description="Copy code/identifier"),
    })