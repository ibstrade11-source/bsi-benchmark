from dataclasses import dataclass

from bsi_benchmark.ab.llm.adapter import LLMAdapter


@dataclass(slots=True)
class ABRunResult:
    baseline: str
    treatment: str


class ABRunner:

    def __init__(self, baseline: LLMAdapter, treatment: LLMAdapter):
        self.baseline = baseline
        self.treatment = treatment

    def run(self, prompt: str) -> ABRunResult:
        return ABRunResult(
            baseline=self.baseline.generate(prompt),
            treatment=self.treatment.generate(prompt),
        )


# Backward compatibility
class ABExperimentRunner:

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def run(self, *args, **kwargs):
        return {}
