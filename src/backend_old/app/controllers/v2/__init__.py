from flask import Blueprint
from flask_restx import Api
from ..common import Controller

def register_v2_controller(blueprint, api):
    # type: (Blueprint, Api) -> Blueprint

    v2_controller = Controller("v2", __name__, url_prefix="")

    from .patrons import patrons_controller
    from .titles import titles_controller
    from .borrows import borrows_controller

    for subcontroller in [
        patrons_controller,
        titles_controller,
        borrows_controller,
    ]:
        v2_controller.register_controller(subcontroller)

    v2_controller.bind(blueprint, api)

    return blueprint
