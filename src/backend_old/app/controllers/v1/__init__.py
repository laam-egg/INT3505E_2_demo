from flask import Blueprint
from flask_restx import Api
from ..common import Controller

def register_v1_controller(blueprint, api):
    # type: (Blueprint, Api) -> Blueprint

    v1_controller = Controller("v1", __name__, url_prefix="")

    from .patrons import patrons_controller
    from .titles import titles_controller
    from .borrows import borrows_controller

    for subcontroller in [
        patrons_controller,
        titles_controller,
        borrows_controller,
    ]:
        v1_controller.register_controller(subcontroller)

    v1_controller.bind(blueprint, api)
    
    return blueprint
