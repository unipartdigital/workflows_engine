from ...utils import func_factory, make_identifier
from ...core import components
from . import defaults


__all__ = (
    "info",
    "complete",
)

info = func_factory(defaults.info, components.InfoComponent, make_identifier)
complete = func_factory(defaults.complete, components.CompleteComponent, make_identifier)
