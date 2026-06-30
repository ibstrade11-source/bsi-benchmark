"""
OpenAlex provider.
"""

from urllib.parse import quote

from bsi_benchmark.network import HttpClient

from .base import Provider
from .registry import registry


class OpenAlexProvider(Provider):

    name = "openalex"

    BASE_URL = "https://api.openalex.org/works"

    def __init__(self):
        self.client = HttpClient()

    def search(self, query: str, rows: int = 5):

        url = (
            f"{self.BASE_URL}"
            f"?search={quote(query)}"
            f"&per-page={rows}"
        )

        response = self.client.get(url)

        if not response.ok:
            return []

        return response.body


registry.register(OpenAlexProvider)
