"""
Provider-neutral API execution facade.

All external API callers can use this module without knowing which
provider/model/network implementation is underneath.
"""

from __future__ import annotations

from typing import Any

from bsi_benchmark.utils.resilient_http import (
    PermanentRequestError,
    RetryableRequestError,
    post_json,
    request,
)


DEFAULT_TIMEOUT = 120.0
DEFAULT_ATTEMPTS = 5


def execute_json_post(
    url: str,
    payload: dict[str, Any],
    headers: dict[str, str] | None = None,
    *,
    timeout: float = DEFAULT_TIMEOUT,
    attempts: int = DEFAULT_ATTEMPTS,
) -> dict[str, Any]:
    return post_json(
        url,
        payload,
        headers,
        timeout=timeout,
        attempts=attempts,
    )


__all__ = [
    "DEFAULT_TIMEOUT",
    "DEFAULT_ATTEMPTS",
    "PermanentRequestError",
    "RetryableRequestError",
    "execute_json_post",
    "request",
]
