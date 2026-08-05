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

from datetime import datetime, timezone

from bsi_benchmark.errors import ProviderError
from bsi_benchmark.generation.manager import GeneratorManager
from bsi_benchmark.models.analyzed_article import AnalyzedArticle
from bsi_benchmark.evaluation.bsi import BSIEvaluator
from bsi_benchmark.evaluation.llm_judge import LLMJudge

from .result import ComparisonCell, ComparisonResult, ComparisonReport


class CrossModelRunner:

    def __init__(
        self,
        generator_manager=None,
        evaluator=None,
        judge=None,
    ):
        self.generator_manager = generator_manager or GeneratorManager()
        self.evaluator = evaluator or BSIEvaluator()
        self.judge = LLMJudge(self.generator_manager.create(judge)) if judge else None

    def run(self, dataset, spec, source_url=None, run_metadata=None) -> ComparisonReport:
        if self.judge is None and getattr(spec, "judge", None):
            self.judge = LLMJudge(
                self.generator_manager.create(spec.judge)
            )

        results = []

        for article in dataset.articles:
            cells = []

            for generator_name in spec.generators:
                generator = self.generator_manager.create(generator_name)

                generated = {}

                for mode, template in spec.prompt_modes.items():
                    analysis, scores = self._generate_one(
                        article,
                        generator,
                        generator_name,
                        mode,
                        template,
                    )

                    generated[mode] = (analysis, scores)

                judge_result = None

                if self.judge and "raw" in generated and "bsi" in generated:
                    raw_analysis = generated["raw"][0]
                    bsi_analysis = generated["bsi"][0]

                    if raw_analysis and bsi_analysis:
                        try:
                            judge_result = self.judge.compare(
                                article=article,
                                raw_analysis=raw_analysis,
                                bsi_analysis=bsi_analysis,
                            )
                        except Exception as exc:
                            judge_result = {"error": str(exc)}

                for mode in generated:
                    analysis, scores = generated[mode]

                    cells.append(
                        ComparisonCell(
                            generator=generator_name,
                            mode=mode,
                            analysis=analysis,
                            scores=scores,
                            judge_result=judge_result,
                        )
                    )

            results.append(ComparisonResult(article=article, cells=cells))

        dataset_name = getattr(dataset, "query", None) or getattr(dataset, "name", "unnamed")
        return ComparisonReport(
            dataset_name=dataset_name, results=results,
            source_url=source_url, run_metadata=run_metadata,
        )


    def _generate_one(self, article, generator, generator_name, mode, template):
        try:
            analysis = generator.generate(article, template)

            if analysis is not None and analysis.generated_at is None:
                analysis.generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        except ProviderError as e:
            return None, {"error": str(e)}

        analyzed = AnalyzedArticle(
            article=article,
            analysis=analysis,
        )

        eval_result = self.evaluator.evaluate(analyzed)

        return analysis, eval_result.scores



