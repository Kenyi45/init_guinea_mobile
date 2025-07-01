"""Domain exceptions for the hexagonal architecture."""


class DomainException(Exception):
    """Base domain exception."""
    pass


class ValidationError(DomainException):
    """Raised when domain validation fails."""
    pass


class NotFoundError(DomainException):
    """Raised when an entity is not found."""
    pass


class AlreadyExistsError(DomainException):
    """Raised when trying to create an entity that already exists."""
    pass


class UnauthorizedError(DomainException):
    """Raised when access is unauthorized."""
    pass 