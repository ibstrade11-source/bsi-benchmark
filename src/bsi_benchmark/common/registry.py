"""
Generic name -> class registry.

The codebase previously had five near-identical hand-written registries
(providers, parsers, evaluation, metrics, reporting), each ~15-25 lines of
copy-pasted dict-wrapping code. This shared generic version is used by the
new `generation` module so that mistake isn't repeated a sixth time.
(Migrating the existing five to use this is a reasonable follow-up refactor,
but is out of scope here to avoid touching more surface area than this
change needs.)
"""

from typing import Dict, Generic, List, TypeVar

T = TypeVar("T")


class Registry(Generic[T]):

    def __init__(self):
        self._items: Dict[str, T] = {}

    def register(self, name: str, item: T) -> None:
        self._items[name] = item

    def get(self, name: str) -> T:
        if name not in self._items:
            raise KeyError(
                f"'{name}' is not registered. Available: {self.names()}"
            )
        return self._items[name]

    def names(self) -> List[str]:
        return sorted(self._items.keys())
