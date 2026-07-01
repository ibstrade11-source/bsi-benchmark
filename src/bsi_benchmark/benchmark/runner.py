from bsi_benchmark.pipeline import PipelineRunner
from bsi_benchmark.evaluation import EvaluationEngine
from bsi_benchmark.reporting import ReportManager

from .result import BenchmarkResult


class BenchmarkRunner:

    def __init__(self):
        self.pipeline = PipelineRunner()
        self.evaluation = EvaluationEngine()
        self.reporting = ReportManager()

    def run(
        self,
        provider,
        query,
        evaluator="basic",
        reporter="json",
    ):
        dataset = self.pipeline.run(provider, query)

        evaluation = self.evaluation.evaluate(
            evaluator,
            dataset,
        )

        report = self.reporting.generate(
            reporter,
            evaluation,
        )

        return BenchmarkResult(
            dataset=dataset,
            evaluation=evaluation,
            report=report,
        )
