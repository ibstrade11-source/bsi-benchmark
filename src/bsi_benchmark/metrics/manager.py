from .registry import registry


class MetricsManager:
    def __init__(self):
        self.registry = registry

    def compute_all(self, dataset):
        metrics = []
        for name in self.registry.names():
            metrics.append(self.registry.get(name)())

        return metrics
