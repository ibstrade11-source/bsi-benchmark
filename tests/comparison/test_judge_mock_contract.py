from types import SimpleNamespace

from bsi_benchmark.comparison.judge import LLMJudge
from bsi_benchmark.generation.mock import MockGenerator
from bsi_benchmark.models.analysis import Analysis


def test_mock_generator_exercises_real_llm_judge_validation():
    article = SimpleNamespace(
        title="Test Article",
        abstract="A deterministic offline test article.",
        doi=None,
    )

    generator = MockGenerator()
    raw = Analysis(
        text="A concise factual analysis.",
        source_model="mock",
        generated_at=None,
    )
    bsi = Analysis(
        text=(
            "Manifest [FACT]\n"
            "Latent [INFERENCE]\n"
            "Meta [SPECULATION]"
        ),
        source_model="mock",
        generated_at=None,
    )

    result = LLMJudge(generator).compare(
        article=article,
        raw_analysis=raw,
        bsi_analysis=bsi,
    )

    assert result["criteria_source"] == "llm"
    assert len(result["criteria"]) == 5
    assert result["weight_sum"] == 100
    assert result["total_scores"]["bsi"] > result["total_scores"]["raw"]
    assert result["bsi_capability_assessment"]["relevance"] == "high"
    assert result["bsi_capability_assessment"]["realization"] == "high"
    assert result["incremental_value"] == "high"
    assert "judge_error" not in result
