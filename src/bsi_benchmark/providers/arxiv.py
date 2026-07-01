"""
arXiv provider.
"""

import time
from urllib.parse import quote

from bsi_benchmark.network import HttpClient
from bsi_benchmark.errors import ProviderUnavailable

from .base import Provider
from .registry import registry


class ArxivProvider(Provider):

    name = "arxiv"

    BASE_URL = "https://export.arxiv.org/api/query"

    def __init__(self):
        self.client = HttpClient()

    def search(self, query: str, rows: int = 5):

        url = (
            f"{self.BASE_URL}"
            f"?search_query=all:{quote(query)}"
            f"&start=0"
            f"&max_results={rows}"
        )

        response = None

        for attempt in range(3):
            response = self.client.get(url)

            if response.ok:
                return response.body

            if response.status_code == 429 or response.status_code >= 500:
                if attempt < 2:
                    time.sleep(2 ** attempt)
                    continue

            raise ProviderUnavailable(
                f"arXiv HTTP {response.status_code}: {response.body}"
            )

        raise ProviderUnavailable(
            f"arXiv HTTP {response.status_code}: {response.body}"
        )


registry.register(ArxivProvider)
