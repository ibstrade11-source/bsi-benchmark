import json

from .base import Parser
from bsi_benchmark.models.article import Article


class CrossrefParser(Parser):

    def parse(self, raw):

        data = json.loads(raw)

        articles = []

        items = data["message"]["items"]

        for item in items:

            title = ""

            if item.get("title"):
                title = item["title"][0]

            articles.append(
                Article(
                    title=title,
                    abstract=item.get("abstract"),
                    doi=item.get("DOI"),
                    url=item.get("URL"),
                )
            )

        return articles

from .registry import registry

registry.register("crossref", CrossrefParser())
