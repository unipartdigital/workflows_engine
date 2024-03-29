from functools import partial

from ...core import components
from ...utils import func_factory, make_identifier
from . import defaults

__all__ = (
    "submit",
    "next",
    "back",
    "reset",
    "close",
    "open_resource",
)


_make_identifier = partial(make_identifier, suffixes=["buttons"])

submit = func_factory(defaults.submit, components.Button, _make_identifier)
next = func_factory(defaults.next, components.Button, _make_identifier)
back = func_factory(defaults.back, components.Button, _make_identifier)
reset = func_factory(defaults.reset, components.Button, _make_identifier)
close = func_factory(defaults.close, components.Button, _make_identifier)
# Button action to open the url in destination_path attribute into a new page
open_resource = func_factory(defaults.open_resource, components.Button, _make_identifier)
