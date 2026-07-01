"""
Crossref provider.
"""

import time
from urllib.parse import quote

from bsi_benchmark.network import HttpClient
from bsi_benchmark.errors import ProviderUnavailable

from .base import Provider
from .registry import registry


class CrossrefProvider(Provider):

    name = "crossref"

    BASE_URL = "https://api.crossref.org/works"

    def __init__(self):
        self.client = HttpClient()

    def search(self, query: str, rows: int = 5):

        url = (
            f"{self.BASE_URL}"
            f"?query={quote(query)}"
            f"&rows={rows}"
        )

        response = None

        for attempt in range(3):
            response = self.client.get(url)

            if response.ok:
                return response.body

            if response.status_code >= 500 and attempt < 2:
                time.sleep(2 ** attempt)
                continue

            break

        raise ProviderUnavailable(
            f"Crossref HTTP {response.status_code}: {response.body}"
        )


registry.register(CrossrefProvider)
