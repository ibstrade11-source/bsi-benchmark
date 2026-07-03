from bsi_benchmark.ab.experiment.engine import ExperimentEngine
from bsi_benchmark.ab.runner import ABRunner
from bsi_benchmark.ab.llm.adapter import LLMAdapter
from bsi_benchmark.ab.llm.base import BaseLLM


class Baseline(BaseLLM):

    def generate(self, prompt):
        return "baseline"


class Treatment(BaseLLM):

    def generate(self, prompt):
        return "treatment"


def test_engine():

    runner = ABRunner(
        LLMAdapter(Baseline()),
        LLMAdapter(Treatment()),
    )

    engine = ExperimentEngine(runner)

    result = engine.run("AI")

    assert result.prompt == "AI"
    assert result.baseline == "baseline"
    assert result.treatment == "treatment"
