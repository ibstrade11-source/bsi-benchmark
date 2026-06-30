"""
Provider manager.
"""

from .registry import registry


class ProviderManager:

    def available(self):
        return registry.names()

    def create(self, name):
        cls = registry.get(name)
        return cls()
