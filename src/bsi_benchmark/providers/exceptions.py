class ProviderError(Exception):
    """Base provider exception."""


class ProviderUnavailable(ProviderError):
    """Provider unavailable."""


class InvalidResponse(ProviderError):
    """Provider returned invalid data."""
