from bsi_benchmark.ab.runner import ABRunner
from .result import ExperimentResult


class ExperimentEngine:

    def __init__(self, runner: ABRunner):
        self.runner = runner

    def run(self, prompt: str) -> ExperimentResult:

        result = self.runner.run(prompt)

        return ExperimentResult(
            prompt=prompt,
            baseline=result.baseline,
            treatment=result.treatment,
        )
