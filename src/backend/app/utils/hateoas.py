"""
Utility for HATEOAS.
"""

from flask_restx import Model, OrderedModel, Namespace, fields
from typing import Any, Callable
from ..db import serialize_mongo_doc

class HATEOAS:
    def __init__(
        self,
        api, # type: Namespace
    ):
        self.api = api
    
    def returns(
        self,
        model,              # type: Model | OrderedModel
        self_links,         # type: Callable[[Any], list[str]]
        collection_links,   # type: Callable[[Any], list[str]]
        as_list=False,
        *args, **kwargs,
    ):
        """
        self_links and collection_links callbacks accept the
        returned content of the original controller method, then
        return the relevant links for HATEOAS. (The content
        has been passed through serialize_mongo_doc.)
        """

        api = self.api
        hateoas_model = api.model(
            name = model.name + ("" if not as_list else "List") + "_HATEOAS",
            model = {
                "content": fields.Nested(model) if not as_list else fields.List(fields.Nested(model)),
                "_links": fields.Nested(
                    api.model("_links", {
                        "self": fields.List(fields.String()),
                        "collection": fields.List(fields.String()),
                    })
                ),
            }
        )

        def decorator(func):
            wrap_with_marshalling = api.marshal_with(hateoas_model, *args, **kwargs)

            def wrapper(*args, **kwargs):
                content = func(*args, **kwargs)
                content = serialize_mongo_doc(content)
                return {
                    "content": content,
                    "_links": {
                        "self": self_links(content),
                        "collection": collection_links(content),
                    },
                }
            
            return wrap_with_marshalling(wrapper)
        return decorator
