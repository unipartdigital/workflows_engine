__all__ = (
    "default",
    "info",
    "error",
    "warning",
    "success",
)

default = dict(identifier="default_message", message_type="default", template="This is question mark")
info = dict(identifier="info_message", message_type="info", template="This is infomation")
warning = dict(identifier="info_message", message_type="warning", template="This is a warning")
error = dict(identifier="info_message", message_type="error", template="Something went wrong")
success = dict(identifier="success_screen", message_type="success", template="Success")
