"""
OpenAlex provider.
"""

from urllib.parse import quote

from bsi_benchmark.network import HttpClient
from bsi_benchmark.errors import ProviderUnavailable

from .base import Provider
from .registry import registry


class OpenAlexProvider(Provider):

    name = "openalex"

    BASE_URL = "https://api.openalex.org/works"

    def __init__(self):
        self.client = HttpClient()

    def get_work(self, work_id: str):
        """Retrieve one exact OpenAlex Work by ID or OpenAlex URL."""
        work_id = str(work_id).strip().rstrip("/")
        if "/" in work_id:
            work_id = work_id.rsplit("/", 1)[-1]

        url = f"{self.BASE_URL}/{quote(work_id)}"
        response = self.client.get(url)
        if not response.ok:
            raise ProviderUnavailable(
                f"OpenAlex HTTP {response.status_code}: {response.body}"
            )
        return response.body

    def search(self, query: str, rows: int = 5):

        url = (
            f"{self.BASE_URL}"
            f"?search={quote(query)}"
            f"&per-page={rows}"
        )

        response = self.client.get(url)

        if not response.ok:
            raise ProviderUnavailable(
                f"OpenAlex HTTP {response.status_code}: {response.body}"
            )

        return response.body


registry.register(OpenAlexProvider)
