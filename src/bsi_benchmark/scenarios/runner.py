from .result import ScenarioResult
from bsi_benchmark.benchmark import BenchmarkRunner


class ScenarioRunner:

    def __init__(self):
        self.runner = BenchmarkRunner()

    def run(self, name, provider, queries):

        results = []

        for query in queries:
            results.append(
                self.runner.run(
                    provider,
                    query,
                )
            )

        return ScenarioResult(
            name=name,
            results=results,
        )
