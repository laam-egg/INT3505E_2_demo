from ....common import Controller, fields

def borrow_dto(controller):
    # type: (Controller) -> any
    return controller.dto("Borrow", {
        "id": fields.String(readonly=True, description="The borrow ID"),
        "patronId": fields.String(required=True, description="The patron ID"),
        "copyId": fields.String(required=True, description="The copy ID"),
        "status": fields.String(required=True, description="Borrow status: BORROWING, RETURNED, or LOST"),
        "createdAt": fields.String(readonly=True, description="Borrow creation timestamp"),
        "statusLastUpdatedAt": fields.String(readonly=True, description="Last status update timestamp"),
    })

def borrow_create_dto(controller):
    # type: (Controller) -> any
    return controller.dto("BorrowCreate", {
        "patronId": fields.String(required=True, description="The patron ID"),
        "copyId": fields.String(required=True, description="The copy ID"),
    }, write=True)

def borrow_update_dto(controller):
    # type: (Controller) -> any
    return controller.dto("BorrowUpdate", {
        "status": fields.String(required=True, description="New borrow status: BORROWING, RETURNED, or LOST"),
    }, write=True)
