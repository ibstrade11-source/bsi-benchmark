"""
Generator manager, mirroring providers/manager.py's pattern for consistency.
"""

from .registry import registry


class GeneratorManager:

    def available(self):
        return registry.names()

    def create(self, name, **kwargs):
        cls = registry.get(name)
        return cls(**kwargs)
