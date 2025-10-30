import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.product import Product  # noqa: E501
from openapi_server.models.product_create import ProductCreate  # noqa: E501
from openapi_server.models.user import User  # noqa: E501
from openapi_server.models.user_create import UserCreate  # noqa: E501
from openapi_server import util


def products_get():  # noqa: E501
    """List all Products

     # noqa: E501


    :rtype: Union[List[Product], Tuple[List[Product], int], Tuple[List[Product], int, Dict[str, str]]
    """
    return 'do some magic!'


def products_post(body):  # noqa: E501
    """Create a new Product

     # noqa: E501

    :param product_create: 
    :type product_create: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    product_create = body
    if connexion.request.is_json:
        product_create = ProductCreate.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def users_get():  # noqa: E501
    """List all users

     # noqa: E501


    :rtype: Union[List[User], Tuple[List[User], int], Tuple[List[User], int, Dict[str, str]]
    """
    return 'do some magic!'


def users_post(body):  # noqa: E501
    """Create a new user

     # noqa: E501

    :param user_create: 
    :type user_create: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    user_create = body
    if connexion.request.is_json:
        user_create = UserCreate.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
