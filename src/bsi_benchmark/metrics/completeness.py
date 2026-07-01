from .base import Metric
from .registry import registry


class CompletenessMetric(Metric):

    name = "completeness"

    def evaluate(self, dataset):

        if dataset.size == 0:
            return 0.0

        complete = sum(
            1
            for article in dataset.articles
            if article.title and article.abstract
        )

        return complete / dataset.size


registry.register(CompletenessMetric())
