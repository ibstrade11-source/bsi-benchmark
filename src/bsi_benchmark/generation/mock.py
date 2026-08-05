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


    def generate_raw(self, article, prompt: str) -> Analysis:
        if "Return ONLY valid JSON" in prompt or "Required structure" in prompt:
            text = """{
  "winner": "bsi",
  "criteria": [
    {
      "name": "depth",
      "importance": 5,
      "raw_score": 5,
      "bsi_score": 8,
      "reason": "BSI analysis shows deeper structure."
    }
  ],
  "total_scores": {
    "raw": 5,
    "bsi": 8
  },
  "reasoning": "BSI provided a stronger structured analysis."
}"""
            return Analysis(text=text, source_model=self.name)

        is_bsi_mode = "bsi" in prompt.lower() or "لایه" in prompt

        if is_bsi_mode:
            text = (
                f"لایه Manifest (آشکار): [FACT] {article.title} "
                f"discusses: {article.abstract}"
            )
        else:
            text = f"{article.title}: {article.abstract}"

        return Analysis(text=text, source_model=self.name)

    def generate(self, article, prompt_template: str) -> Analysis:
        rendered = render(prompt_template, article)
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
