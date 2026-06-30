"""
Base interface for all providers.
"""

from abc import ABC
from abc import abstractmethod


class Provider(ABC):

    name: str

    @abstractmethod
    def search(self, query: str):
        raise NotImplementedError
