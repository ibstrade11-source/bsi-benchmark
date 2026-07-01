class MetricRegistry:

    def __init__(self):
        self._metrics = {}

    def register(self, metric):

        self._metrics[metric.name] = metric

    def get(self, name):

        return self._metrics[name]

    def available(self):

        return sorted(self._metrics.keys())


registry = MetricRegistry()
