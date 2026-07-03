"""
CrossModelRunner: the automated benchmark engine.

For every article in a Dataset, for every (generator, prompt_mode) pair in
a ComparisonSpec: call the generator to produce an Analysis, wrap it with
the article into an AnalyzedArticle, and score it with BSIEvaluator. The
result is a ComparisonReport with one cell per (article, generator, mode)
combination, ready to render as a table (see comparison/reporter.py) or
export as JSON for further analysis.

A failure calling any one generator (missing API key, rate limit, network
error) is caught and recorded as a failed cell rather than raising -- one
bad combination should not lose the results for everything else in a
multi-hour benchmark run.
"""

from bsi_benchmark.errors import ProviderError
from bsi_benchmark.evaluation.bsi import BSIEvaluator
from bsi_benchmark.generation.manager import GeneratorManager
from bsi_benchmark.models.analyzed_article import AnalyzedArticle

from .result import ComparisonCell, ComparisonResult, ComparisonReport


class CrossModelRunner:

    def __init__(self, generator_manager=None, evaluator=None):
        self.generator_manager = generator_manager or GeneratorManager()
        self.evaluator = evaluator or BSIEvaluator()

    def run(self, dataset, spec, source_url=None) -> ComparisonReport:
        results = []

        for article in dataset.articles:
            cells = []

            for generator_name in spec.generators:
                generator = self.generator_manager.create(generator_name)

                for mode, template in spec.prompt_modes.items():
                    cell = self._run_one(article, generator, generator_name, mode, template)
                    cells.append(cell)

            results.append(ComparisonResult(article=article, cells=cells))

        dataset_name = getattr(dataset, "query", None) or getattr(dataset, "name", "unnamed")
        return ComparisonReport(dataset_name=dataset_name, results=results, source_url=source_url)

    def _run_one(self, article, generator, generator_name, mode, template) -> ComparisonCell:
        try:
            analysis = generator.generate(article, template)
        except ProviderError as e:
            return ComparisonCell(
                generator=generator_name, mode=mode, analysis=None,
                scores={"error": str(e)},
            )

        analyzed = AnalyzedArticle(article=article, analysis=analysis)
        eval_result = self.evaluator.evaluate(analyzed)

        return ComparisonCell(
            generator=generator_name, mode=mode,
            analysis=analysis, scores=eval_result.scores,
        )
