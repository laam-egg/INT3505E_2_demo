from .common import Controller

api_controller = Controller("api/v1", __name__)

from .patrons import patrons_controller
from .titles import titles_controller

for subcontroller in [
    patrons_controller,
    titles_controller,
]:
    api_controller.register_controller(subcontroller)
