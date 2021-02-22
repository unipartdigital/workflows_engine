from itertools import chain
import string

__all__ = ("make_identifier", "func_factory", "container_factory")


def make_identifier(attrs, suffixes=None, black_list=("flow_attrs",)):
    parts = [
        str(v).lower().replace(" ", "_") for k, v in attrs.items() if k not in black_list and v is not None
    ]
    return remove_punctuation("_".join(parts + (suffixes or [])), allowed="_")


def container_factory(defaults, base_container):
    """ Produces a function which produces a  based on the default values """

    def func(**kwargs):
        attrs = defaults.copy()
        attrs.update(kwargs)
        return base_container(**attrs)

    return func


def func_factory(defaults, base_component, make_identifier):
    """ Produces a function which produces a  based on the default values """

    def func(**kwargs):
        attrs = defaults.copy()
        attrs.update(kwargs)
        if kwargs and not kwargs.get("identifier"):
            attrs.update({"identifier": make_identifier(attrs)})
        return base_component(**attrs)

    return func


def remove_punctuation(original_string, allowed):
    to_remove = string.punctuation.translate(str.maketrans("", "", allowed))
    return original_string.translate(str.maketrans("", "", to_remove))
