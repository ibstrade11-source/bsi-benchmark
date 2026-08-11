"""
Network-related exceptions.
"""

class NetworkError(Exception):
    """Base network exception."""


class RequestFailed(NetworkError):
    """HTTP request failed."""


class InvalidResponse(NetworkError):
    """Invalid server response."""
