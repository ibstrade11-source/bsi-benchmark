import requests

from .base import Provider

class ArxivProvider(Provider):

    name="arxiv"

    URL="https://export.arxiv.org/api/query"

    def search(self,domain,limit):

        r=requests.get(

            self.URL,

            params={

                "search_query":domain,

                "start":0,

                "max_results":limit

            },

            timeout=(10,120)

        )

        r.raise_for_status()

        return r.text
