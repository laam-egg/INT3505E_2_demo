from ....common import Controller, fields

def title_dto(controller):
    # type: (Controller) -> any
    return controller.dto("Title", {
        "id": fields.String(readonly=True, description="The title ID"),
        "name": fields.String(required=True, description="Title name"),
        "edition": fields.Integer(required=True, description="Edition number"),
        "authors": fields.String(required=True, description="Newline-separated list of authors"),
        "yearOfPublication": fields.Integer(required=True, description="Year of publication"),
        "tags": fields.String(required=True, description="Newline-separated list of tags"),
        "totalCopies": fields.Integer(readonly=True, description="Total number of copies"),
        "availableCopies": fields.Integer(readonly=True, description="Number of available copies"),
        "borrowedCopies": fields.Integer(readonly=True, description="Number of borrowed copies"),
        "lostCopies": fields.Integer(readonly=True, description="Number of lost copies"),
    })

def title_create_dto(controller):
    # type: (Controller) -> any
    return controller.dto("TitleCreate", {
        "name": fields.String(required=True, description="Title name"),
        "edition": fields.Integer(required=True, description="Edition number"),
        "authors": fields.String(required=True, description="Newline-separated list of authors"),
        "yearOfPublication": fields.Integer(required=True, description="Year of publication"),
        "tags": fields.String(required=True, description="Newline-separated list of tags"),
    })

def title_update_dto(controller):
    # type: (Controller) -> any
    return controller.dto("TitleUpdate", {
        "name": fields.String(description="Title name"),
        "edition": fields.Integer(description="Edition number"),
        "authors": fields.String(description="Newline-separated list of authors"),
        "yearOfPublication": fields.Integer(description="Year of publication"),
        "tags": fields.String(description="Newline-separated list of tags"),
    })