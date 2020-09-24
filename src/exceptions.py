class InvalidArguments(Exception):
    """ Unwanted arguments.
    Example: When you try to use 'path' and 'value' on input field where only one is allowed."""

    def __init__(self, msg):
        pass
