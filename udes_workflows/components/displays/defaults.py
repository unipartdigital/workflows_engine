__all__ = (
    "info",
    "error",
    "warning",
    "complete",
)

info = dict(identifier="info_msg", msg_type="info", msg_template="This is infomation")
warning = dict(identifier="info_msg", msg_type="warning", msg_template="This is a warning")
error = dict(identifier="info_msg", msg_type="error", msg_template="Something went wrong")
complete = dict(identifier="complete_screen", msg_type="complete", msg_template="Complete")
