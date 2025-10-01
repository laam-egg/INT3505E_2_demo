from .common import Controller

api_controller = Controller("api/v1", __name__)

from .patrons import patrons_controller
from .titles import titles_controller
from .borrows import borrows_controller

for subcontroller in [
    patrons_controller,
    titles_controller,
    borrows_controller,
]:
    api_controller.register_controller(subcontroller)
