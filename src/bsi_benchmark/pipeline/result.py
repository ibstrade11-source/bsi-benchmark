from dataclasses import dataclass, field
from bsi_benchmark.models.article import Article


@dataclass
class PipelineResult:
    provider: str
    query: str
    articles: list[Article]
    skipped_count: int = 0
    skipped_titles: list[str] = field(default_factory=list)

    # Retrieval validation / audit trail.
    retrieval_status: str = "accepted"
    retrieval_validation: dict = field(default_factory=dict)
    rejected_articles: list[dict] = field(default_factory=list)
