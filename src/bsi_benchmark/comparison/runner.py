"""
CrossModelRunner: the automated benchmark engine.

For every article in a Dataset and every (generator, prompt_mode) pair in
a ComparisonSpec: call the generator to produce an Analysis, then -- once
both the "raw" and "bsi" analyses exist for that article -- send both to
an independent LLM judge (see comparison/judge.py) rather than scoring
each analysis in isolation. The result is a ComparisonReport with one
cell per (article, generator, mode) combination, ready to render as a
table (see comparison/reporter.py) or export as JSON for further
analysis.

A failure calling any one generator (missing API key, rate limit, network
error) is caught and recorded as a failed cell rather than raising -- one
bad combination should not lose the results for everything else in a
multi-hour benchmark run.
"""
from bsi_benchmark.ab.client import BSIApiClient
from datetime import datetime, timezone

from bsi_benchmark.errors import ProviderError
from bsi_benchmark.generation.manager import GeneratorManager

from .result import ComparisonCell, ComparisonResult, ComparisonReport
from .judge import LLMJudge


class CrossModelRunner:

    def __init__(self, generator_manager=None, judge=None):
        self.generator_manager = generator_manager or GeneratorManager()
        # `judge` may be a generator NAME (str, e.g. from --judge) or an
        # already-built LLMJudge instance. If neither this nor spec.judge
        # is given, falls back to LLMJudge(generator=None), which always
        # uses the honestly-labeled keyword heuristic.
        self._explicit_judge = judge

    def _build_judge(self, spec) -> LLMJudge:
        if isinstance(self._explicit_judge, LLMJudge):
            return self._explicit_judge

        judge_model = self._explicit_judge or getattr(spec, "judge", None)
        if judge_model:
            return LLMJudge(self.generator_manager.create(judge_model))

        return LLMJudge(generator=None)

    def run(self, dataset, spec, source_url=None, run_metadata=None) -> ComparisonReport:
        judge = self._build_judge(spec)
        results = []

        for article in dataset.articles:
            cells = []

            for generator_name in spec.generators:
                generator = self.generator_manager.create(generator_name)

                generated = {}
                for mode, template in spec.prompt_modes.items():
                    analysis, metadata = self._generate_one(
                        article, generator, generator_name, mode, template,
                    )
                    generated[mode] = (analysis, metadata)

                judge_result = None
                if "raw" in generated and "bsi" in generated:
                    raw_analysis = generated["raw"][0]
                    bsi_analysis = generated["bsi"][0]
                    if raw_analysis and bsi_analysis:
                        try:
                            judge_result = judge.compare(
                                article=article,
                                raw_analysis=raw_analysis,
                                bsi_analysis=bsi_analysis,
                            )
                        except Exception as exc:
                            judge_result = {"error": str(exc)}

                for mode, (analysis, metadata) in generated.items():
                    cells.append(
                        ComparisonCell(
                            generator=generator_name,
                            mode=mode,
                            analysis=analysis,
                            metadata=metadata,
                            judge_result=judge_result,
                            scores={"BSI": 0.5},
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

        return analysis, {}
