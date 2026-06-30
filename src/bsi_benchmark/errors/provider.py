"""
Provider related exceptions.
"""

from .base import BSIBenchmarkError


class ProviderError(BSIBenchmarkError):
    pass


class ProviderTimeout(ProviderError):
    pass


class ProviderUnavailable(ProviderError):
    pass


class ProviderRateLimit(ProviderError):
    pass


class InvalidProviderResponse(ProviderError):
    pass
