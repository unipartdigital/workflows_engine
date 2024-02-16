__all__ = (
    "submit",
    "next",
    "back",
    "reset",
    "close",
    "open_resource",
)

submit = dict(identifier="submit_button", action="submit", style="primary", text="Submit",)
next = dict(identifier="next_button", action="next", style="primary", text="Next",)
back = dict(identifier="back_button", action="back", style="default", text="Back",)
reset = dict(identifier="restart_button", action="reset", style="primary", text="Continue",)
close = dict(identifier="close_button", action="close", style="primary", text="Close",)
open_resource = dict(identifier="open_resource_button", action="open_resource", style="primary", text="Open Resource",)
