from dataclasses import dataclass

from .article import Article
from .analysis import Analysis


@dataclass(slots=True)
class AnalyzedArticle:
    article: Article
    analysis: Analysis

    @property
    def source_text(self) -> str:
        """Raw text the analysis should be checked against: full text when available, otherwise title + abstract."""
        title = self.article.title or ""
        abstract = self.article.abstract or ""
        full_text = self.article.full_text or ""
        if full_text.strip():
            return full_text
        return f"{title}\n{abstract}"
