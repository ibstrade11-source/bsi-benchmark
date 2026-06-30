"""
Crossref provider.
"""

from urllib.parse import quote

from bsi_benchmark.network import HttpClient

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

        response = self.client.get(url)

        if not response.ok:
            return []

        data = response.body

        return data


registry.register(CrossrefProvider)
