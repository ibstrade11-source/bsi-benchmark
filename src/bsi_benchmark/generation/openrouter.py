"""
OpenRouterGenerator: calls OpenRouter's unified API (OpenAI-compatible).

Requires the OPENROUTER_API_KEY environment variable. Get a free key
(no credit card) at https://openrouter.ai/keys

Why this backend exists: one key, many models. OpenRouter routes to
models from NVIDIA, Google, OpenAI, Cohere, Poolside, and others.
Free models have IDs ending in :free -- the list rotates, so verify
current availability at https://openrouter.ai/models before relying
on a specific model ID.

Default model: nvidia/nemotron-3-ultra-550b-a55b:free
(confirmed free and reachable, Aug 2026)
"""

import json
import os

from bsi_benchmark.network import HttpClient
from bsi_benchmark.models.analysis import Analysis
from bsi_benchmark.errors import ProviderUnavailable, InvalidProviderResponse

from .base import AnalysisGenerator
from .prompt import render

API_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = os.environ.get(
    "OPENROUTER_MODEL",
    "nvidia/nemotron-3-ultra-550b-a55b:free"
)
DEFAULT_MAX_TOKENS = 2000


class OpenRouterGenerator(AnalysisGenerator):

    name = "openrouter"

    def __init__(self, model: str = DEFAULT_MODEL, max_tokens: int = DEFAULT_MAX_TOKENS):
        self.model = model
        self.max_tokens = max_tokens
        self.client = HttpClient()

    def generate(self, article, prompt_template: str) -> Analysis:
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            raise ProviderUnavailable(
                "OPENROUTER_API_KEY is not set. Get a free key (no credit "
                "card) at https://openrouter.ai/keys and export it."
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
                f"OpenRouter HTTP {response.status_code}: {response.body}"
            )

        try:
            payload = json.loads(response.body)
            text = payload["choices"][0]["message"]["content"]
        except (json.JSONDecodeError, KeyError, IndexError, TypeError) as exc:
            raise InvalidProviderResponse(
                f"Could not parse OpenRouter response: {exc}"
            ) from exc

        if not text:
            raise InvalidProviderResponse(
                "OpenRouter response contained no text content."
            )

        return Analysis(text=text, source_model=self.model)
