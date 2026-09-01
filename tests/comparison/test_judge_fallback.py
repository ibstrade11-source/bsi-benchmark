from types import SimpleNamespace

from bsi_benchmark.comparison.judge import LLMJudge
from bsi_benchmark.models.analysis import Analysis


class BrokenJudgeGenerator:
    name = "broken-judge"

    def generate(self, article, prompt_template):
        return Analysis(
            text="THIS IS NOT VALID JSON",
            source_model=self.name,
            generated_at=None,
        )


def test_invalid_llm_judge_response_uses_explicit_heuristic_fallback():
    article = SimpleNamespace(
        title="Fallback Test Article",
        abstract="A deterministic fallback test article.",
        doi=None,
    )

    raw = Analysis(
        text="A concise factual analysis.",
        source_model="test",
        generated_at=None,
    )
    bsi = Analysis(
        text=(
            "Manifest [FACT]\n"
            "Latent [INFERENCE]\n"
            "Meta [SPECULATION]"
        ),
        source_model="test",
        generated_at=None,
    )

    result = LLMJudge(BrokenJudgeGenerator()).compare(
        article=article,
        raw_analysis=raw,
        bsi_analysis=bsi,
    )

    assert result["criteria_source"] == "heuristic_fallback"
    assert result["judge_failure_stage"] == "llm_compare"
    assert "judge_error" in result
    assert result["judge_error"]
    assert "heuristic" in result["reasoning"].lower()
    assert result["bsi_capability_assessment"]["incremental_value"] == "none"
    assert result["incremental_value"] == "none"
