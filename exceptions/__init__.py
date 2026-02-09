"""Domain exception hierarchy for MEDirect Edge."""


class MEDirectError(Exception):
    """Base exception for all MEDirect domain errors."""

    def __init__(self, message: str = "An error occurred"):
        self.message = message
        super().__init__(self.message)


class NotFoundError(MEDirectError):
    """Raised when a requested resource does not exist."""
    pass


class ValidationError(MEDirectError):
    """Raised when input fails domain validation rules."""
    pass


class InvalidStateError(MEDirectError):
    """Raised when an operation is invalid for the current entity state."""
    pass


class ExternalServiceError(MEDirectError):
    """Raised when an external service call fails."""
    pass