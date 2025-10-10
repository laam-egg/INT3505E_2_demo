from ..common import Controller

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
