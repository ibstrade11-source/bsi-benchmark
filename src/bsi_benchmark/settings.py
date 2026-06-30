"""
Runtime settings.
"""

from dataclasses import dataclass

from .config import DEFAULT_TIMEOUT
from .config import DEFAULT_USER_AGENT


@dataclass(slots=True)
class Settings:
    timeout: int = DEFAULT_TIMEOUT
    user_agent: str = DEFAULT_USER_AGENT


settings = Settings()
