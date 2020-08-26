from ...utils import func_factory, make_identifier
from ...core import components
from . import defaults


__all__ = (
    "info",
    "warning",
    "error",
    "complete",
)

info = func_factory(defaults.info, components.MessageBox, make_identifier)
warning = func_factory(defaults.warning, components.MessageBox, make_identifier)
error = func_factory(defaults.error, components.MessageBox, make_identifier)
complete = func_factory(defaults.complete, components.MessageBox, make_identifier)
