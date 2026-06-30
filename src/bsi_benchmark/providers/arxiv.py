"""
arXiv provider.
"""

from urllib.parse import quote

from bsi_benchmark.network import HttpClient

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

        response = self.client.get(url)

        if not response.ok:
            return []

        return response.body


registry.register(ArxivProvider)
