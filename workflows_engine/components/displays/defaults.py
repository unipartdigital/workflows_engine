__all__ = (
    "default",
    "info",
    "error",
    "warning",
    "success",
)

default = dict(message_type="default", template="This is question mark")
info = dict(message_type="info", template="This is infomation")
warning = dict(message_type="warning", template="This is a warning")
error = dict(message_type="error", template="Something went wrong")
success = dict(message_type="success", template="Success")
