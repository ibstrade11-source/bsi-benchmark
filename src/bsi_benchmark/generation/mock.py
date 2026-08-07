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
      "name": "depth",
      "raw_score": 5,
      "bsi_score": 8,
      "reason": "BSI analysis shows deeper structure."
    }
  ],
  "winner": "bsi",
  "reasoning": "BSI provided a stronger structured analysis."
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
