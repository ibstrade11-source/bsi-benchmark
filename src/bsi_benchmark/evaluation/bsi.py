from dataclasses import dataclass


@dataclass
class BSIScore:
    coverage: float
    completeness: float
    signal_quality: float
    total: float


class BSIEvaluator:
    def evaluate(self, dataset):
        articles = dataset.articles

        if not articles:
            return BSIScore(0, 0, 0, 0)

        coverage = min(len(articles) / 5.0, 1.0)

        completeness = sum(
            1 for a in articles if a.abstract and a.doi
        ) / len(articles)

        signal_quality = sum(
            1 for a in articles if a.title and len(a.title) > 10
        ) / len(articles)

        total = 0.4 * coverage + 0.3 * completeness + 0.3 * signal_quality

        return BSIScore(
            coverage=coverage,
            completeness=completeness,
            signal_quality=signal_quality,
            total=total,
        )
