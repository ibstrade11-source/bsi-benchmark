"""
MockGenerator: deterministic, offline, no-network generator for tests and
for developing/debugging the orchestration pipeline (comparison/runner.py)
without spending real API calls. Not a substitute for real model output --
never use this generator's scores as an actual benchmark result.
"""

from bsi_benchmark.models.analysis import Analysis

from .base import AnalysisGenerator
from .prompt import render


class MockGenerator(AnalysisGenerator):

    name = "mock"

    def generate(self, article, prompt_template: str) -> Analysis:
        rendered = render(prompt_template, article)

        # Judge-style prompts (see comparison/judge.py) ask for a JSON
        # verdict, not an analysis -- detect that by the same "Return
        # ONLY valid JSON" marker judge.py's prompt uses, so MockGenerator
        # can stand in as a self-judge offline (no real LLM/API key),
        # exercising the same code path self-judging uses in production.
        if "Return ONLY valid JSON" in rendered:
            text = """{
  "criteria": [
    {
      "name": "structural_layers",
      "importance": 30,
      "raw_score": 5,
      "bsi_score": 8,
      "reason": "Structural organization is highly important for comparing these analyses."
    },
    {
      "name": "epistemic_separation",
      "importance": 20,
      "raw_score": 5,
      "bsi_score": 8,
      "reason": "Separating factual content from inference is important for this evaluation."
    },
    {
      "name": "uncertainty_awareness",
      "importance": 20,
      "raw_score": 5,
      "bsi_score": 8,
      "reason": "Recognition of uncertainty materially affects analytical quality."
    },
    {
      "name": "evidence_grounding",
      "importance": 15,
      "raw_score": 6,
      "bsi_score": 8,
      "reason": "Evidence grounding is relevant to judging the reliability of the analysis."
    },
    {
      "name": "analysis_depth",
      "importance": 15,
      "raw_score": 5,
      "bsi_score": 9,
      "reason": "Analytical coverage provides an important measure of comparative quality."
    }
  ],
  "bsi_capability_assessment": {
    "relevance": "high",
    "realization": "high",
    "incremental_value": "high",
    "reason": "The structured BSI analysis provides additional observable analytical depth."
  },
  "winner": "bsi",
  "incremental_value": "high",
  "reasoning": "The BSI analysis provides stronger structured and epistemically separated analysis."
}"""
            return Analysis(text=text, source_model=self.name)

        is_bsi_mode = "bsi" in rendered.lower() or "لایه" in rendered

        if is_bsi_mode:
            text = (
                f"لایه Manifest (آشکار): [FACT] {article.title} "
                f"discusses: {article.abstract}\n"
                "لایه Latent (پنهان): [INFERENCE] If the stated method is "
                "valid, assuming its core assumptions hold, the conclusion "
                "follows conditionally.\n"
                "لایه Meta (فرا): [SPECULATION] It may generalize further; "
                "this suggests future work could extend the implications."
            )
        else:
            text = f"{article.title}: {article.abstract}"

        return Analysis(text=text, source_model=self.name)
