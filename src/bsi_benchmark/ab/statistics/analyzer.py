from statistics import mean


class StatisticalAnalyzer:

    def summarize(self, scores):

        if not scores:
            return {
                "count": 0,
                "mean": 0.0,
                "min": 0.0,
                "max": 0.0,
            }

        return {
            "count": len(scores),
            "mean": mean(scores),
            "min": min(scores),
            "max": max(scores),
        }
