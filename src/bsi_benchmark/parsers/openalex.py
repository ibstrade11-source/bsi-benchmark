import json

from .base import Parser
from bsi_benchmark.models.article import Article


class OpenAlexParser(Parser):

    def parse(self, raw):

        data = json.loads(raw)

        articles = []

        for item in data["results"]:

            articles.append(
                Article(
                    title=item.get("title"),
                    abstract=None,
                    doi=item.get("doi"),
                    url=item.get("id"),
                )
            )

        return articles

from .registry import registry

registry.register("openalex", OpenAlexParser())
