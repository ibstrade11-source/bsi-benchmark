"""
Provider registry.
"""

from __future__ import annotations

from typing import Dict, Type

from .base import Provider


class ProviderRegistry:
    def __init__(self):
        self._providers: Dict[str, Type[Provider]] = {}

    def register(self, provider: Type[Provider]) -> None:
        self._providers[provider.name] = provider

    def get(self, name: str) -> Type[Provider]:
        return self._providers[name]

    def names(self):
        return sorted(self._providers.keys())


registry = ProviderRegistry()
