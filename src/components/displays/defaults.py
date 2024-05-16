__all__ = (
    "default",
    "info",
    "error",
    "warning",
    "success",
)

default = dict(
    identifier="default_message",
    message_type="default",
    template="This is question mark",
    background_color="unset",
)
info = dict(
    identifier="info_message",
    message_type="info",
    template="This is infomation",
    background_color="#d9d9d9",
)
warning = dict(
    identifier="info_message",
    message_type="warning",
    template="This is a warning",
    background_color="#ffba19",
)
error = dict(
    identifier="info_message",
    message_type="error",
    template="Something went wrong",
    background_color="#ff1314",
)
success = dict(
    identifier="success_screen",
    message_type="success",
    template="Success",
    background_color="#66fd7f",
)
