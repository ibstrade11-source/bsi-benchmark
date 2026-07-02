from bsi_benchmark.providers import ProviderManager

from bsi_benchmark.parsers.crossref import CrossrefParser
from bsi_benchmark.parsers.openalex import OpenAlexParser
from bsi_benchmark.parsers.arxiv import ArxivParser
from bsi_benchmark.parsers.mock import MockParser

from .result import PipelineResult


class PipelineRunner:

    def __init__(self):

        self.providers = ProviderManager()

        self.parsers = {
            "crossref": CrossrefParser(),
            "openalex": OpenAlexParser(),
            "arxiv": ArxivParser(),
            "mock": MockParser(),
        }

    def run(self, provider_name, query):

        provider = self.providers.create(provider_name)

        raw = provider.search(query)

        parser = self.parsers[provider_name]

        articles = parser.parse(raw)

        return PipelineResult(
            provider=provider_name,
            query=query,
            articles=articles,
        )
