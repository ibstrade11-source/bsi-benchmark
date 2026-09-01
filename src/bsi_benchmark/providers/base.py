"""
Base provider interface.

Providers expose capabilities polymorphically.  The benchmark orchestration
must never inspect provider names to decide which operations are supported.
"""

from abc import ABC, abstractmethod


class Provider(ABC):

    name: str

    @abstractmethod
    def search(self, query: str):
        raise NotImplementedError

    def fetch_fulltext(self, article) -> str | None:
        """
        Optional full-text capability.

        A provider that can retrieve full text should override this method.
        Providers that cannot must return None rather than forcing the CLI
        or runner to branch on provider names.
        """
        return None

    @property
    def full_text_source(self) -> str:
        return self.name
