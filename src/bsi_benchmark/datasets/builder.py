from bsi_benchmark.pipeline import PipelineRunner

from .dataset import Dataset


class DatasetBuilder:

    def __init__(self):

        self.runner = PipelineRunner()

    def build(self, provider, query):

        result = self.runner.run(provider, query)

        return Dataset(
            query=query,
            provider=provider,
            articles=result.articles,
        )
