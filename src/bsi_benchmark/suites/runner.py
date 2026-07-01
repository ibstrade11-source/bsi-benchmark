from .result import SuiteResult
from bsi_benchmark.scenarios import ScenarioRunner


class SuiteRunner:

    def __init__(self):
        self.runner = ScenarioRunner()

    def run(self, name, provider_queries):

        scenarios = []

        for provider, queries in provider_queries.items():

            scenarios.append(
                self.runner.run(
                    provider,
                    provider,
                    queries,
                )
            )

        return SuiteResult(
            name=name,
            scenarios=scenarios,
        )
