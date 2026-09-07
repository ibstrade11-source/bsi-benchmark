from bsi_benchmark.providers import ProviderManager
from bsi_benchmark.parsers.crossref import CrossrefParser
from bsi_benchmark.parsers.openalex import OpenAlexParser
from bsi_benchmark.parsers.arxiv import ArxivParser
from bsi_benchmark.parsers.mock import MockParser
from bsi_benchmark.parsers.europepmc import EuropePMCParser
from bsi_benchmark.parsers.semantic_scholar import SemanticScholarParser

from .result import PipelineResult
from .retrieval import validate_candidates


class PipelineRunner:
    def __init__(self):
        self.providers = ProviderManager()
        self.parsers = {
            "crossref": CrossrefParser(),
            "openalex": OpenAlexParser(),
            "arxiv": ArxivParser(),
            "europepmc": EuropePMCParser(),
            "semantic_scholar": SemanticScholarParser(),
            "mock": MockParser(),
            "single_article": MockParser(),
        }

    def run(self, provider_name, query, limit=None, article_id=None):
        provider = self.providers.create(provider_name)

        if article_id is not None:
            if provider_name != "openalex":
                raise ValueError(
                    "--article-id is currently supported only with "
                    "--provider openalex"
                )
            if not hasattr(provider, "get_work"):
                raise ValueError(
                    f"Provider '{provider_name}' does not support exact "
                    "article retrieval"
                )
            raw = provider.get_work(article_id)
        else:
            raw = provider.search(query)

        parser = self.parsers[provider_name]
        articles = parser.parse(raw)

        # First remove records that cannot possibly be benchmark inputs.
        valid_articles = []
        skipped_titles = []

        for article in articles:
            title_ok = bool((article.title or "").strip())
            abstract_ok = bool((article.abstract or "").strip())

            if title_ok and abstract_ok:
                valid_articles.append(article)
            else:
                skipped_titles.append(article.title or "(untitled)")

        # Retrieval validation happens BEFORE --limit so a mismatched
        # top result cannot consume the requested article slot.
        validated_articles, rejected_articles, retrieval = validate_candidates(
            query,
            valid_articles,
        )

        if limit is not None:
            validated_articles = validated_articles[:limit]

        return PipelineResult(
            provider=provider_name,
            query=query,
            articles=validated_articles,
            skipped_count=len(skipped_titles),
            skipped_titles=skipped_titles,
            retrieval_status=retrieval.get("retrieval_status", "accepted"),
            retrieval_validation=retrieval,
            rejected_articles=rejected_articles,
        )
