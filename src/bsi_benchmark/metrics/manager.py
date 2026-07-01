from .registry import registry


class MetricManager:

    def available(self):

        return registry.available()

    def evaluate(self, dataset):

        results = {}

        for name in registry.available():

            metric = registry.get(name)

            results[name] = metric.evaluate(dataset)

        return results
