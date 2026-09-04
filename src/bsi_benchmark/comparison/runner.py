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

Checkpoint/resume: when `checkpoint_path` is given, per-cell analyses and
per-generator judge results are persisted to that file as the run
progresses (see comparison/checkpoint.py). Re-running with the same
checkpoint_path:
  - never re-calls a generator for an analysis that already succeeded;
  - re-runs the judge for any cell whose judge result is missing, errored,
    or fell back to the keyword heuristic, overwriting that invalid entry;
  - leaves a cell whose judge result already came from a real LLM judge
    untouched.
"""
import time
from datetime import datetime, timezone
from dataclasses import replace as _dataclasses_replace

from bsi_benchmark.errors import ProviderError
from bsi_benchmark.generation.manager import GeneratorManager
from bsi_benchmark.generation.compaction import compact_full_text

from . import checkpoint as checkpointing
from .result import ComparisonCell, ComparisonResult, ComparisonReport
from .judge import LLMJudge


# Substrings seen in real provider error messages for "this single
# request is too large / would exceed a per-minute token budget" --
# deliberately provider-agnostic (Groq, OpenRouter, or any future
# generator all phrase this differently, so we match on the shared
# vocabulary rather than a specific provider's exact wording).
_TOKEN_BUDGET_ERROR_MARKERS = (
    "rate_limit_exceeded",
    "tokens per minute",
    "request too large",
    "reduce your message size",
    "context_length_exceeded",
    "maximum context length",
)


def _looks_like_token_budget_error(exc: Exception) -> bool:
    text = str(exc).lower()
    return any(marker in text for marker in _TOKEN_BUDGET_ERROR_MARKERS)


_COMPACTION_BUDGET_ESCALATION = (6000, 1500, 300)


class CrossModelRunner:

    def __init__(self, generator_manager=None, judge=None):
        self.generator_manager = generator_manager or GeneratorManager()
        # `judge` may be a generator NAME (str, e.g. from --judge) or an
        # already-built LLMJudge instance.
        #
        # Priority when building the judge for a given cell:
        #   1. an explicit LLMJudge instance passed to __init__
        #   2. an explicit judge generator NAME (--judge / spec.judge)
        #   3. self-judging: the SAME generator that produced this cell's
        #      raw/bsi analyses judges its own output (this is the
        #      documented default -- see the --judge help text in cli.py)
        #   4. only if a generator instance truly isn't available does this
        #      fall through to LLMJudge(generator=None), the honestly
        #      labeled keyword heuristic -- this should not happen in
        #      normal operation since step 3 always has a generator.
        self._explicit_judge = judge

    def _build_judge(self, spec, self_generator=None) -> LLMJudge:
        if isinstance(self._explicit_judge, LLMJudge):
            return self._explicit_judge

        judge_model = self._explicit_judge or getattr(spec, "judge", None)
        if judge_model:
            judge_kwargs = {}

            # Explicit judge model is intentionally independent from the
            # generator model. If no model is supplied, the generator's
            # normal/default model remains unchanged.
            explicit_model = getattr(spec, "judge_model", None)
            if explicit_model:
                judge_kwargs["model"] = explicit_model

            return LLMJudge(
                self.generator_manager.create(judge_model, **judge_kwargs)
            )

        # IMPORTANT:
        # Preserve existing self-judge behavior exactly.
        if self_generator is not None:
            return LLMJudge(self_generator)

        return LLMJudge(generator=None)

    def run(self, dataset, spec, source_url=None, run_metadata=None,
            checkpoint_path=None) -> ComparisonReport:
        checkpoint = None
        if checkpoint_path:
            checkpoint = checkpointing.load_checkpoint(checkpoint_path)
        if checkpoint is None:
            checkpoint = checkpointing.new_checkpoint()

        def _save_checkpoint():
            if checkpoint_path:
                checkpointing.save_checkpoint(checkpoint_path, checkpoint)

        results = []

        for article in dataset.articles:
            art_key = checkpointing.article_key(article)
            cells = []

            for generator_name in spec.generators:
                try:
                    generator = self.generator_manager.create(generator_name)
                except Exception as exc:
                    cells.append(
                        ComparisonCell(
                            generator=generator_name,
                            mode="error",
                            analysis=None,
                            metadata={"error": f"generator initialization failed: {exc}"},
                            judge_result=None,
                            failed=True,
                            scores={},
                        )
                    )
                    continue

                # Built per-generator so that, absent an explicit judge,
                # each generator judges its own raw-vs-bsi output.
                try:
                    judge = self._build_judge(spec, self_generator=generator)
                except Exception as exc:
                    judge = None
                    judge_init_error = str(exc)
                else:
                    judge_init_error = None

                generated = {}
                for mode, template in spec.prompt_modes.items():
                    ckey = checkpointing.cell_key(art_key, generator_name, mode)
                    cached_cell = checkpoint["cells"].get(ckey)

                    if cached_cell and not cached_cell.get("failed") and cached_cell.get("analysis"):
                        analysis, metadata, _ = checkpointing.cell_from_dict(cached_cell)
                    else:
                        analysis, metadata = self._generate_one(
                            article, generator, generator_name, mode, template,
                        )
                        checkpoint["cells"][ckey] = checkpointing.cell_to_dict(
                            analysis, metadata, analysis is None,
                        )
                        _save_checkpoint()

                    generated[mode] = (analysis, metadata)

                jkey = checkpointing.judge_key(art_key, generator_name)
                cached_judge = checkpoint["judge_results"].get(jkey)

                if checkpointing.is_valid_judge_result(cached_judge):
                    judge_result = cached_judge
                elif judge_init_error is not None:
                    judge_result = {"error": f"judge initialization failed: {judge_init_error}"}
                    checkpoint["judge_results"][jkey] = judge_result
                    _save_checkpoint()
                elif "raw" in generated and "bsi" in generated:
                    raw_analysis = generated["raw"][0]
                    bsi_analysis = generated["bsi"][0]
                    judge_result = None
                    if raw_analysis and bsi_analysis:
                        try:
                            judge_result = judge.compare(
                                article=article,
                                raw_analysis=raw_analysis,
                                bsi_analysis=bsi_analysis,
                            )
                        except Exception as exc:
                            judge_result = {"error": str(exc)}
                    checkpoint["judge_results"][jkey] = judge_result
                    _save_checkpoint()
                else:
                    judge_result = cached_judge

                for mode, (analysis, metadata) in generated.items():
                    cell_failed = analysis is None
                    cells.append(
                        ComparisonCell(
                            generator=generator_name,
                            mode=mode,
                            analysis=analysis,
                            metadata=metadata,
                            judge_result=judge_result,
                            failed=cell_failed,
                            scores=(
                                {}
                                if cell_failed
                                else (
                                    {
                                        "RAW": round(float(judge_result["total_scores"].get("raw", 0)) / 10, 3),
                                        "BSI": round(float(judge_result["total_scores"].get("bsi", 0)) / 10, 3),
                                    }
                                    if judge_result and "total_scores" in judge_result
                                    else {}
                                )
                            ),
                        )
                    )

            results.append(
                ComparisonResult(article=article, cells=cells, article_id=art_key)
            )

        dataset_name = getattr(dataset, "query", None) or getattr(dataset, "name", "unnamed")
        return ComparisonReport(
            dataset_name=dataset_name, results=results,
            source_url=source_url, run_metadata=run_metadata,
        )

    def _generate_one(self, article, generator, generator_name, mode, template):
        # Execution Burden per METHODOLOGY.md section 32: wall-clock time
        # and provider-reported token usage are recorded alongside quality
        # results, never fabricated (section 63) -- elapsed time is timed
        # here directly (always genuine, regardless of provider), and
        # token usage is copied through only when the provider's response
        # actually included a usage object (Analysis.usage; None otherwise,
        # see generation/groq.py and generation/openrouter.py).
        start = time.monotonic()

        def _elapsed() -> float:
            return round(time.monotonic() - start, 3)

        try:
            analysis = generator.generate(article, template)
            if analysis is not None and analysis.generated_at is None:
                analysis.generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        except ProviderError as e:
            full_text = getattr(article, "full_text", None)
            if not (_looks_like_token_budget_error(e) and full_text):
                return None, {"error": str(e), "execution_time_seconds": _elapsed()}

            last_error = e
            for budget_chars in _COMPACTION_BUDGET_ESCALATION:
                compacted_article = _dataclasses_replace(
                    article,
                    full_text=compact_full_text(full_text, budget_chars=budget_chars),
                )
                try:
                    analysis = generator.generate(compacted_article, template)
                    if analysis is not None and analysis.generated_at is None:
                        analysis.generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                    return analysis, {
                        "token_budget_fallback": True,
                        "token_budget_fallback_chars": budget_chars,
                        "original_error": str(e),
                        "execution_time_seconds": _elapsed(),
                        "usage": getattr(analysis, "usage", None),
                    }
                except ProviderError as e2:
                    if not _looks_like_token_budget_error(e2):
                        return None, {
                            "error": str(e2),
                            "token_budget_fallback_attempted": True,
                            "original_error": str(e),
                            "execution_time_seconds": _elapsed(),
                        }
                    last_error = e2
                    continue

            return None, {
                "error": str(last_error),
                "token_budget_fallback_attempted": True,
                "token_budget_fallback_budgets_tried": list(_COMPACTION_BUDGET_ESCALATION),
                "original_error": str(e),
                "execution_time_seconds": _elapsed(),
            }

        return analysis, {
            "execution_time_seconds": _elapsed(),
            "usage": getattr(analysis, "usage", None),
        }
