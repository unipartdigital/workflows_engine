__all__ = (
    "info",
    "error",
    "warning",
    "complete",
)

info = dict(identifier="info_msg", msg_type="info", template="This is infomation")
warning = dict(identifier="info_msg", msg_type="warning", template="This is a warning")
error = dict(identifier="info_msg", msg_type="error", template="Something went wrong")
complete = dict(identifier="complete_screen", msg_type="complete", template="Complete")
