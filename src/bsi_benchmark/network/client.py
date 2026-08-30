"""
HTTP client.
"""

import requests

from bsi_benchmark.config import DEFAULT_TIMEOUT
from bsi_benchmark.config import DEFAULT_USER_AGENT

from .response import Response
from .retry import retry


class HttpClient:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers["User-Agent"] = DEFAULT_USER_AGENT

    def get(self, url: str):

        def operation():
            r = self.session.get(
                url,
                timeout=DEFAULT_TIMEOUT,
            )

            return Response(
                status_code=r.status_code,
                url=r.url,
                body=r.text,
            )

        return retry(operation, should_retry=self._should_retry)

    def get_bytes(self, url: str) -> bytes:
        """
        Fetch raw binary content at `url` (e.g. a PDF) and return the
        response body as bytes. Unlike get(), the body is never decoded
        as text -- decoding binary content (e.g. via r.text) silently
        corrupts it, which is why this is a separate method rather than
        a flag on get().
        """

        def operation():
            r = self.session.get(
                url,
                timeout=DEFAULT_TIMEOUT,
            )

            return Response(
                status_code=r.status_code,
                url=r.url,
                body="",
                content=r.content,
            )

        response = retry(operation, should_retry=self._should_retry)

        if not response.ok:
            from bsi_benchmark.errors import ProviderUnavailable
            raise ProviderUnavailable(
                f"GET {url} -> HTTP {response.status_code}"
            )

        return response.content

    def post(self, url: str, json_body: dict, headers: dict | None = None, timeout: int | None = None):

        def operation():
            r = self.session.post(
                url,
                json=json_body,
                headers=headers,
                timeout=timeout or DEFAULT_TIMEOUT,
            )

            return Response(
                status_code=r.status_code,
                url=r.url,
                body=r.text,
            )

        return retry(operation, should_retry=self._should_retry)

    @staticmethod
    def _should_retry(response: Response) -> bool:
        # Retry on server errors and rate limiting; do NOT retry on 4xx
        # client errors (bad request, bad auth, not found, etc.) since
        # those will not succeed on repetition.
        return response.status_code >= 500 or response.status_code == 429
