from .base import BaseLLM
from bsi_benchmark.ab.client import BSIApiClient


class BSILLMAdapter(BaseLLM):

    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.client = BSIApiClient(base_url)

    def generate(self, prompt: str) -> str:

        result = self.client.analyze_llm(prompt)

        if "final_synthesis" in result:
            return result["final_synthesis"]

        if "error" in result:
            raise RuntimeError(result["error"])

        raise RuntimeError("Unexpected API response")
