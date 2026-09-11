class NotFoundError(Exception):
    """Raised when a requested domain entity does not exist."""


class MetadataResolutionError(Exception):
    """Raised when metadata cannot be resolved for a URL."""
