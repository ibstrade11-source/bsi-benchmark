"""
Normalized HTTP response.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class Response:
    status_code: int
    url: str
    body: str
    content: bytes = b""

    @property
    def ok(self) -> bool:
        return 200 <= self.status_code < 300
