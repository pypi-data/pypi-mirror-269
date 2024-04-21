class BadRequest(Exception):
    """Raise when user input was incorrect."""


class DoesNotExist(Exception):
    """Raise when entity was not found in database."""


class AlreadyExists(Exception):
    """Raise when an object passed to application already exists."""


class Unauthorized(Exception):
    """Raise when authentication fails."""
