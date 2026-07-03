from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class ABResponse:
    provider: str
    query: str
    use_bsi: bool
    result: dict[str, Any]
