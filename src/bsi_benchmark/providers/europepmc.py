"""
Europe PMC provider.
"""

from urllib.parse import quote

from bsi_benchmark.network import HttpClient

from .base import Provider
from .registry import registry


class EuropePMCProvider(Provider):

    name = "europepmc"

    BASE_URL = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"

    def __init__(self):
        self.client = HttpClient()

    def search(self, query: str, rows: int = 5):

        url = (
            f"{self.BASE_URL}"
            f"?query={quote(query)}"
            f"&pageSize={rows}"
            f"&format=json"
        )

        response = self.client.get(url)

        if not response.ok:
            return []

        return response.body


registry.register(EuropePMCProvider)
