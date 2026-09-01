"""
Retry utilities.

Centralized retry logic. Retries on:
  1. Any raised exception (network-level failures: timeout, connection reset).
  2. Any result for which `should_retry(result)` returns True (e.g. an HTTP
     response object with a 5xx / 429 status code that was returned normally,
     not raised as an exception).

This fixes a defect where HTTP error responses (which are returned as normal
values, not exceptions, by HttpClient) silently bypassed retry entirely.
"""

import time


def retry(operation, attempts=3, delay=1, should_retry=None):
    """
    Args:
        operation: zero-arg callable to invoke.
        attempts: max number of attempts.
        delay: base delay in seconds; backs off exponentially (delay * 2**n).
        should_retry: optional predicate(result) -> bool. If provided, a
            successful (non-exception) return value is also checked against
            this predicate; if True, the operation is retried.
    """
    last_error = None
    last_result = None

    for attempt in range(attempts):
        try:
            result = operation()
        except Exception as exc:
            last_error = exc
            if attempt < attempts - 1:
                time.sleep(delay * (2 ** attempt))
            continue

        if should_retry is not None and should_retry(result):
            last_result = result
            if attempt < attempts - 1:
                time.sleep(delay * (2 ** attempt))
            continue

        return result

    if last_error is not None:
        raise last_error

    return last_result
