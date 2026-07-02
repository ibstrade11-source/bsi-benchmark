from dataclasses import dataclass

from .article import Article
from .analysis import Analysis


@dataclass(slots=True)
class AnalyzedArticle:
    article: Article
    analysis: Analysis

    @property
    def source_text(self) -> str:
        """Raw text the analysis should be checked against: title + abstract."""
        title = self.article.title or ""
        abstract = self.article.abstract or ""
        return f"{title}\n{abstract}"
