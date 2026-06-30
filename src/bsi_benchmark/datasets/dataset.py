from dataclasses import dataclass, field

from bsi_benchmark.models.article import Article


@dataclass
class Dataset:

    query: str

    provider: str

    articles: list[Article] = field(default_factory=list)

    @property
    def size(self):

        return len(self.articles)
