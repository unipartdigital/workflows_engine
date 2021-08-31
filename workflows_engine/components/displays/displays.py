from ...utils import func_factory, make_identifier
from ...core import components
from . import defaults


__all__ = (
    "default",
    "info",
    "warning",
    "error",
    "success",
)

default = func_factory(defaults.default, components.MessageBox, make_identifier)
info = func_factory(defaults.info, components.MessageBox, make_identifier)
warning = func_factory(defaults.warning, components.MessageBox, make_identifier)
error = func_factory(defaults.error, components.MessageBox, make_identifier)
success = func_factory(defaults.success, components.MessageBox, make_identifier)
