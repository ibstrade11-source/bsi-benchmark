from bsi_benchmark.pipeline import PipelineRunner
from bsi_benchmark.reporting import ReportManager

from .result import BenchmarkResult


class BenchmarkRunner:
    def __init__(self):
        self.pipeline = PipelineRunner()
        self.reporting = ReportManager()

    def run(
        self,
        provider,
        query,
        reporter="json",
    ):
        dataset = self.pipeline.run(provider, query)

        report = self.reporting.generate(
            reporter,
            dataset,
        )

        return BenchmarkResult(
            dataset=dataset,
            evaluation=None,
            report=report,
        )
