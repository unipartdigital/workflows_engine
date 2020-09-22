__all__ = (
    "info",
    "error",
    "warning",
    "success",
)

info = dict(identifier="info_message", message_type="info", template="This is infomation")
warning = dict(identifier="info_message", message_type="warning", template="This is a warning")
error = dict(identifier="info_message", message_type="error", template="Something went wrong")
success = dict(identifier="success_screen", message_type="success", template="Success")
