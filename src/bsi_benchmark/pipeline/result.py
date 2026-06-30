from dataclasses import dataclass
from bsi_benchmark.models.article import Article


@dataclass
class PipelineResult:
    provider: str
    query: str
    articles: list[Article]
