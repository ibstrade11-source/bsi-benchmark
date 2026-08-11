"""Provider-neutral resilient execution for independent LLM judges."""

from __future__ import annotations

import json
import os
import urllib.request
from typing import Any

from bsi_benchmark.utils.resilient_http import request


def execute_judge_request(
    url: str,
    payload: dict[str, Any],
    *,
    api_key: str,
    timeout: float = 120.0,
    attempts: int = 5,
    extra_headers: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Execute an LLM judge request through the shared resilient HTTP layer."""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    if extra_headers:
        headers.update(extra_headers)

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    response = request(
        req,
        timeout=timeout,
        attempts=attempts,
    )

    try:
        return json.loads(response.body.decode("utf-8"))
    except Exception as exc:
        raise ValueError(
            "Judge HTTP request succeeded but returned invalid JSON"
        ) from exc
