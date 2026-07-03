from .base import BaseLLM


class LLMAdapter:

    def __init__(self, backend: BaseLLM):
        self.backend = backend

    def generate(self, prompt: str) -> str:
        return self.backend.generate(prompt)
