class InvalidMessageException(Exception):
    """Is raised, when invalid/no message is received as a response."""
    pass


class InvalidArgumentException(Exception):
    """Is raised, when an invalid argument/arguments are given to a function"""
    pass
