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

        return retry(operation)
