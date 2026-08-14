from bsi_benchmark.providers import ProviderManager
from bsi_benchmark.parsers.crossref import CrossrefParser
from bsi_benchmark.parsers.openalex import OpenAlexParser
from bsi_benchmark.parsers.arxiv import ArxivParser
from bsi_benchmark.parsers.mock import MockParser
from bsi_benchmark.parsers.europepmc import EuropePMCParser
from bsi_benchmark.parsers.semantic_scholar import SemanticScholarParser

from .result import PipelineResult


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

    def run(self, provider_name, query, limit=None):
        provider = self.providers.create(provider_name)

        raw = provider.search(query)

        parser = self.parsers[provider_name]

        articles = parser.parse(raw)

        # Drop articles with no usable title/abstract *before* applying
        # --limit, not after -- otherwise a --limit N request can silently
        # hand the benchmark N articles that are all missing content while
        # perfectly good results sit further down the provider's list.
        valid_articles = []
        skipped_titles = []
        for article in articles:
            title_ok = bool((article.title or "").strip())
            abstract_ok = bool((article.abstract or "").strip())
            if title_ok and abstract_ok:
                valid_articles.append(article)
            else:
                skipped_titles.append(article.title or "(untitled)")

        if limit is not None:
            valid_articles = valid_articles[:limit]

        return PipelineResult(
            provider=provider_name,
            query=query,
            articles=valid_articles,
            skipped_count=len(skipped_titles),
            skipped_titles=skipped_titles,
        )
