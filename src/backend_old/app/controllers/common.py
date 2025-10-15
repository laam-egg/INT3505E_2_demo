from flask import Flask, Blueprint
from flask_restx import Api, Namespace, Resource, Model, OrderedModel, fields
from typing import Any, Generator
from ..utils.join_prefix import join_prefix

class Controller:
    def __init__(self, name, module_name, url_prefix=None, description="", enable_hateoas=False):
        # type: (Controller, str, str, str | None, str, bool) -> None
        self.Resource = Resource

        if url_prefix is None:
            real_url_prefix = name # "/" + name
        else:
            real_url_prefix = url_prefix
        self._c_url_prefix = real_url_prefix
        self._c_bp_name = name
        self._c_bp_module_name = module_name
        self._c_ns = Namespace(name, description=description)
        self._c_parent_controller = None # type: Controller | None
        self._c_child_controllers = [] # type: list[Controller]
        self._c_enable_hateoas = enable_hateoas
        self._c_name_to_model_map = {}
    
    def get_url_prefix(self):
        return self._c_url_prefix
    
    def get_namespace(self):
        return self._c_ns
    
    def dto(self, name, model, *args, write=False, **kwargs):
        # type: (Controller, str, dict[str, Any], Any, Any) -> Model | OrderedModel
        d = self._c_ns.model(
            *args,
            name=name,
            model=model,
            **kwargs,
        )

        self._c_name_to_model_map[name] = d

        if self._c_enable_hateoas and not write: # only apply HATEOAS for reading!
            name = name + "_HATEOAS"
            d = self._c_ns.model(
                name=name,
                model={
                    "content": fields.Nested(d),
                    "_links": fields.Nested(
                        self._c_ns.model("_links", {
                            "self": fields.List(fields.String()),
                            "collection": fields.List(fields.String()),
                        })
                    ),
                }
            )
            self._c_name_to_model_map[name] = d

        return d
    
    def marshal_with(
        self, # type: Controller
        model, # type: Model | OrderedModel
        *args, **kwargs
    ):
        if self._c_enable_hateoas:
            name = model.name + "_HATEOAS"
            model = self._c_name_to_model_map.get(name, model)

            initial_wrapper = self._c_ns.marshal_with(model, *args, **kwargs)

            def decor(func):
                def wrapper(*args, **kwargs):
                    data = func(*args, **kwargs)
                    return {
                        "content": data,
                        "_links": {
                            "self": ["TO BE DEFINED"],
                            "collection": ["TO BE DEFINED"],
                        },
                    }
                return initial_wrapper(wrapper)
            
            return decor
        else:
            return self._c_ns.marshal_with(model, *args, **kwargs)
    
    def marshal_list_with(
        self, # type: Controller
        model, # type: Model | OrderedModel
        *args, **kwargs
    ):
        if self._c_enable_hateoas:
            name = model.name + "_HATEOAS"
            model = self._c_name_to_model_map.get(name, model)
            initial_wrapper = self._c_ns.marshal_list_with(model, *args, **kwargs)

            def decor(func):
                def wrapper(*args, **kwargs):
                    data = func(*args, **kwargs)
                    return {
                        "content": data,
                        "_links": {
                            "self": ["TO BE DEFINED"],
                            "collection": ["TO BE DEFINED"],
                        },
                    }
                return initial_wrapper(wrapper)
            
            return decor
        else:
            return self._c_ns.marshal_list_with(model, *args, **kwargs)
    
    def enumerate_leaf_controllers_and_full_prefixes(self, prefix):
        # type: (Controller, str | None) -> Generator[tuple[Controller, str], None, None]
        """Generates all of the leaf controllers (i.e. those having no children) as well as their (nested) URL prefixes.
        They could be this controller itself or any of its children/offsprings/etc.
        """
        PREFIX = join_prefix(prefix, self._c_url_prefix)
        if len(self._c_child_controllers) == 0:
            yield (self, PREFIX)

        for subcontroller in self._c_child_controllers:
            for c, p in subcontroller.enumerate_leaf_controllers_and_full_prefixes(PREFIX):
                yield c, p
    
    def set_parent_controller(self, parent_controller):
        # type: (Controller, Controller) -> None
        self._c_parent_controller = parent_controller
    
    def register_controller(self, child_controller, blueprint_options={}):
        # type: (Controller, Controller, dict[str, Any]) -> None
        self._c_child_controllers.append(child_controller)
        child_controller.set_parent_controller(self)
    
    def bind(self, app, api, prefix=None):
        # type: (Controller, Flask, Api, str | None) -> Flask
        for leaf_controller, leaf_prefix in self.enumerate_leaf_controllers_and_full_prefixes(prefix):
            print("LEAF:", leaf_prefix)
            blueprint = Blueprint(
                leaf_controller._c_bp_name,
                leaf_controller._c_bp_module_name,
                url_prefix=leaf_prefix,
            )
            app.register_blueprint(blueprint)
            api.add_namespace(leaf_controller._c_ns, path=leaf_prefix)

        return app
    
    def __getattr__(self, key):
        if isinstance(key, str):
            if key.startswith("_c_") or key in [
                "Resource",
                "__init__",
                "get_url_prefix",
                "get_namespace",
                "get_blueprint",
                "set_parent_controller",
                "register_controller",
                "__getattr__",
                "__setattr__",
                "enumerate_subcontrollers_and_full_prefixes",
                "dto",
                "marshal_with",
                "marshal_list_with",
            ]:
                return super(Controller, self).__getattribute__(self, key)
        return getattr(self._c_ns, key)
