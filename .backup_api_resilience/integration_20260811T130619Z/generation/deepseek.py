"""
DeepSeekGenerator: calls the DeepSeek Chat Completions API (OpenAI-compatible
format, different base URL).

Requires the DEEPSEEK_API_KEY environment variable. Never hardcode a key in
this file or in configs/ -- read it from the environment only.
"""

import json
import os

from bsi_benchmark.network import HttpClient
from bsi_benchmark.models.analysis import Analysis
from bsi_benchmark.errors import ProviderUnavailable, InvalidProviderResponse

from .base import AnalysisGenerator
from .prompt import render

API_URL = "https://api.deepseek.com/chat/completions"
DEFAULT_MODEL = "deepseek-chat"
DEFAULT_MAX_TOKENS = 2000


class DeepSeekGenerator(AnalysisGenerator):

    name = "deepseek"

    def __init__(self, model: str = DEFAULT_MODEL, max_tokens: int = DEFAULT_MAX_TOKENS):
        self.model = model
        self.max_tokens = max_tokens
        self.client = HttpClient()

    def generate(self, article, prompt_template: str) -> Analysis:
        api_key = os.environ.get("DEEPSEEK_API_KEY")
        if not api_key:
            raise ProviderUnavailable(
                "DEEPSEEK_API_KEY is not set. Export it before running "
                "the 'compare' or 'generate' CLI commands."
            )

        prompt = render(prompt_template, article)

        response = self.client.post(
            API_URL,
            json_body={
                "model": self.model,
                "max_tokens": self.max_tokens,
                "messages": [{"role": "user", "content": prompt}],
            },
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
        )

        if not response.ok:
            raise ProviderUnavailable(
                f"DeepSeek HTTP {response.status_code}: {response.body}"
            )

        try:
            payload = json.loads(response.body)
            text = payload["choices"][0]["message"]["content"]
        except (json.JSONDecodeError, KeyError, IndexError, TypeError) as exc:
            raise InvalidProviderResponse(
                f"Could not parse DeepSeek response: {exc}"
            ) from exc

        if not text:
            raise InvalidProviderResponse(
                "DeepSeek response contained no text content."
            )

        return Analysis(text=text, source_model=self.model)
