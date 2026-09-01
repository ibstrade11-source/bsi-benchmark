import json

from bsi_benchmark.models.article import Article
from .base import Parser


class SemanticScholarParser(Parser):
    def parse(self, raw):
        data = json.loads(raw) if isinstance(raw, str) else raw
        articles = []

        for item in data.get("data", []):
            ext = item.get("externalIds") or {}
            articles.append(
                Article(
                    title=item.get("title", ""),
                    abstract=item.get("abstract"),
                    full_text=None,
                    doi=ext.get("DOI"),
                    url=item.get("url"),
                    input_quality={
                        "has_title": bool((item.get("title") or "").strip()),
                        "has_abstract": bool((item.get("abstract") or "").strip()),
                        "has_full_text": False,
                        "source": "semantic_scholar",
                        "enriched": False,
                    },
                )
            )
        return articles
