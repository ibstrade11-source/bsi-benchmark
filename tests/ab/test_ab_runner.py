from bsi_benchmark.ab.runner import ABRunner
from bsi_benchmark.ab.llm.adapter import LLMAdapter
from bsi_benchmark.ab.llm.base import BaseLLM


class DummyBaseline(BaseLLM):

    def generate(self, prompt):
        return "baseline"


class DummyTreatment(BaseLLM):

    def generate(self, prompt):
        return "treatment"


def test_ab_runner():

    runner = ABRunner(
        LLMAdapter(DummyBaseline()),
        LLMAdapter(DummyTreatment()),
    )

    result = runner.run("AI")

    assert result.baseline == "baseline"
    assert result.treatment == "treatment"
