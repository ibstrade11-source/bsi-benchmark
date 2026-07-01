from .context import ExecutionContext


class BenchmarkRunner:

    def __init__(self, context=None):

        self.context = context or ExecutionContext()

    def run(self, dataset):

        return {
            "provider": dataset.provider,
            "query": dataset.query,
            "articles": dataset.size,
            "mode": self.context.mode,
        }
