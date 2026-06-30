"""
Semantic Scholar provider.
"""

from urllib.parse import quote

from bsi_benchmark.network import HttpClient

from .base import Provider
from .registry import registry


class SemanticScholarProvider(Provider):

    name = "semantic_scholar"

    BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

    def __init__(self):
        self.client = HttpClient()

    def search(self, query: str, rows: int = 5):

        fields = "title,abstract,year,externalIds,url"

        url = (
            f"{self.BASE_URL}"
            f"?query={quote(query)}"
            f"&limit={rows}"
            f"&fields={fields}"
        )

        response = self.client.get(url)

        if not response.ok:
            return []

        return response.body


registry.register(SemanticScholarProvider)
