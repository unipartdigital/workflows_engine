from itertools import chain

__all__ = ("make_identifier", "func_factory")


def make_identifier(attrs, suffixes=None, black_list=("flow_attrs",)):
    parts = [k.lower().replace(" ", "_") for k, v in attrs.items() if k not in black_list]
    return "_".join(parts + (suffixes or []))


def func_factory(defaults, base_component, make_identifier):
    """ Produces a function which produces a  based on the default values """

    def func(**kwargs):
        attrs = defaults.copy()
        attrs.update(kwargs)
        if kwargs and not kwargs.get("identifier"):
            attrs.update({"identifier": make_identifier(attrs)})
        return base_component(**attrs)

    return func
