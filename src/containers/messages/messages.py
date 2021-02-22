from ...utils import container_factory
from ...core.containers import Message
from . import defaults

warning = container_factory(defaults.warning, Message)
error = container_factory(defaults.error, Message)
success = container_factory(defaults.success, Message)
