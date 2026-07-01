from .base import Metric
from .registry import registry


class ArticleCountMetric(Metric):

    name = "article_count"

    def evaluate(self, dataset):

        return dataset.size


registry.register(ArticleCountMetric())
