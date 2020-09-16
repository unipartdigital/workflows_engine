__all__ = (
    "info",
    "error",
    "warning",
    "complete",
)

info = dict(identifier="info_message", message_type="info", template="This is infomation")
warning = dict(identifier="info_message", message_type="warning", template="This is a warning")
error = dict(identifier="info_message", message_type="error", template="Something went wrong")
complete = dict(identifier="complete_screen", message_type="complete", template="Complete")
