from .base import Provider
from .registry import registry


class MockProvider(Provider):
    name = "mock"

    def search(self, query: str):
        return [{"title": query}]


registry.register(MockProvider)
