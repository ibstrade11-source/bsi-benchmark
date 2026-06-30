import requests

from .base import Provider

class CrossrefProvider(Provider):

    name = "crossref"

    URL = "https://api.crossref.org/works"

    def search(self, domain, limit):

        r = requests.get(
            self.URL,
            params={
                "query": domain,
                "rows": limit
            },
            timeout=(10,120),
            headers={
                "User-Agent":"BSI Benchmark"
            }
        )

        r.raise_for_status()

        return r.json()["message"]["items"]
