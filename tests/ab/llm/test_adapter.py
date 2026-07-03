from bsi_benchmark.ab.llm.base import BaseLLM
from bsi_benchmark.ab.llm.adapter import LLMAdapter


class DummyLLM(BaseLLM):

    def generate(self, prompt: str) -> str:
        return "dummy-response"


def test_adapter():

    adapter = LLMAdapter(DummyLLM())

    assert adapter.generate("hello") == "dummy-response"
