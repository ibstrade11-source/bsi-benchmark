"""
Provider-neutral resilient HTTP execution.

This module deliberately contains no provider/model-specific logic.
It handles transient network/API failures while preserving the caller's
ability to distinguish retryable failures from permanent failures.
"""

from __future__ import annotations

import json
import random
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Callable


RETRYABLE_HTTP_CODES = {
    408, 425, 429,
    500, 502, 503, 504, 520, 521, 522, 523, 524,
}

RETRYABLE_TEXT = (
    "timed out",
    "timeout",
    "temporarily unavailable",
    "temporary failure",
    "connection reset",
    "connection aborted",
    "connection refused",
    "connection error",
    "name or service not known",
    "temporary failure in name resolution",
    "failed to resolve",
    "dns",
    "network is unreachable",
    "no address associated with hostname",
    "resource exhausted",
    "worker local total request limit",
    "upstream error",
)


class RetryableRequestError(RuntimeError):
    """A request failed in a way that is normally safe to retry."""


class PermanentRequestError(RuntimeError):
    """A request failed and should not be blindly retried."""


@dataclass
class RequestResult:
    status: int
    body: bytes
    attempts: int


def _is_retryable_exception(exc: BaseException) -> bool:
    text = str(exc).lower()

    if isinstance(exc, (TimeoutError, ConnectionError, OSError)):
        return True

    if isinstance(exc, urllib.error.URLError):
        return True

    return any(marker in text for marker in RETRYABLE_TEXT)


def _retry_delay(attempt: int, base: float, maximum: float) -> float:
    # Exponential backoff + small jitter.
    delay = min(maximum, base * (2 ** max(0, attempt - 1)))
    return delay + random.uniform(0.0, min(1.0, delay * 0.25))


def request(
    req: urllib.request.Request,
    *,
    timeout: float = 120.0,
    attempts: int = 5,
    backoff_base: float = 2.0,
    backoff_max: float = 30.0,
    sleeper: Callable[[float], None] = time.sleep,
) -> RequestResult:
    """
    Execute an HTTP request with bounded retry/backoff.

    Important:
    - DNS failures are retryable.
    - connection failures are retryable.
    - timeouts are retryable.
    - rate limiting and common 5xx responses are retryable.
    - other HTTP errors are surfaced immediately.
    - no provider/model/location assumptions are made here.
    """

    attempts = max(1, int(attempts))
    last_exc: BaseException | None = None

    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return RequestResult(
                    status=int(response.status),
                    body=response.read(),
                    attempts=attempt,
                )

        except urllib.error.HTTPError as exc:
            last_exc = exc
            code = int(exc.code)

            try:
                body = exc.read()
            except Exception:
                body = b""

            if code not in RETRYABLE_HTTP_CODES or attempt >= attempts:
                if code in RETRYABLE_HTTP_CODES:
                    raise RetryableRequestError(
                        f"HTTP {code} after {attempt} attempt(s): "
                        f"{body[:2000].decode(errors='replace')}"
                    ) from exc
                raise PermanentRequestError(
                    f"HTTP {code}: "
                    f"{body[:2000].decode(errors='replace')}"
                ) from exc

        except Exception as exc:
            last_exc = exc

            if attempt >= attempts or not _is_retryable_exception(exc):
                if _is_retryable_exception(exc):
                    raise RetryableRequestError(
                        f"{type(exc).__name__} after {attempt} attempt(s): {exc}"
                    ) from exc
                raise

        if attempt < attempts:
            sleeper(_retry_delay(attempt, backoff_base, backoff_max))

    raise RetryableRequestError(
        f"request failed after {attempts} attempt(s): {last_exc}"
    ) from last_exc


def post_json(
    url: str,
    payload: dict[str, Any],
    headers: dict[str, str] | None = None,
    *,
    timeout: float = 120.0,
    attempts: int = 5,
) -> dict[str, Any]:
    """POST JSON using the resilient request layer."""

    hdrs = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    if headers:
        hdrs.update(headers)

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=hdrs,
        method="POST",
    )

    result = request(
        req,
        timeout=timeout,
        attempts=attempts,
    )

    try:
        return json.loads(result.body.decode("utf-8"))
    except Exception as exc:
        raise PermanentRequestError(
            "HTTP request succeeded but response was not valid JSON"
        ) from exc
