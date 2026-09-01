import json

from bsi_benchmark.models.article import Article
from .base import Parser


class EuropePMCParser(Parser):
    def parse(self, raw):
        data = json.loads(raw) if isinstance(raw, str) else raw
        results = data.get("resultList", {}).get("result", [])
        articles = []

        for item in results:
            source = item.get("source")
            article_id = item.get("id")
            url = (
                f"https://europepmc.org/article/{source}/{article_id}"
                if source and article_id
                else None
            )
            articles.append(
                Article(
                    title=item.get("title", ""),
                    abstract=item.get("abstractText"),
                    full_text=None,
                    doi=item.get("doi"),
                    url=url,
                    input_quality={
                        "has_title": bool((item.get("title") or "").strip()),
                        "has_abstract": bool((item.get("abstractText") or "").strip()),
                        "has_full_text": False,
                        "source": "europepmc",
                        "enriched": False,
                    },
                )
            )
        return articles
