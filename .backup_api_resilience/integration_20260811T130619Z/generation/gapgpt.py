"""
GapGptGenerator: calls GapGPT's OpenAI-compatible endpoint.

Requires the GAPGPT_API_KEY environment variable.
Base URL: https://api.gapgpt.app/v1 (OpenAI-compatible chat/completions).
"""

import json
import os

from bsi_benchmark.network import HttpClient
from bsi_benchmark.models.analysis import Analysis
from bsi_benchmark.errors import ProviderUnavailable, InvalidProviderResponse

from .base import AnalysisGenerator
from .prompt import render

API_URL = "https://api.gapgpt.app/v1/chat/completions"
DEFAULT_MODEL = os.environ.get("GAPGPT_MODEL", "gpt-4o-mini")
DEFAULT_MAX_TOKENS = 2000


class GapGptGenerator(AnalysisGenerator):

    name = "gapgpt"

    def __init__(self, model: str = DEFAULT_MODEL, max_tokens: int = DEFAULT_MAX_TOKENS):
        self.model = model
        self.max_tokens = max_tokens
        self.client = HttpClient()

    def generate(self, article, prompt_template: str) -> Analysis:
        api_key = os.environ.get("GAPGPT_API_KEY")
        if not api_key:
            raise ProviderUnavailable(
                "GAPGPT_API_KEY is not set. Export it in ~/.bashrc first."
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
                f"GapGPT HTTP {response.status_code}: {response.body}"
            )

        try:
            payload = json.loads(response.body)
            text = payload["choices"][0]["message"]["content"]
        except (json.JSONDecodeError, KeyError, IndexError, TypeError) as exc:
            raise InvalidProviderResponse(
                f"Could not parse GapGPT response: {exc}"
            ) from exc

        if not text:
            raise InvalidProviderResponse("GapGPT response contained no text content.")

        return Analysis(text=text, source_model=self.model)
