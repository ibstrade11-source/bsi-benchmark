"""
GroqGenerator: calls Groq's Chat Completions API (OpenAI-compatible format).

Requires the GROQ_API_KEY environment variable.
"""

import json
import os

from bsi_benchmark.network import HttpClient
from bsi_benchmark.models.analysis import Analysis
from bsi_benchmark.errors import ProviderUnavailable, InvalidProviderResponse

from .base import AnalysisGenerator
from .prompt import render

API_URL = "https://api.groq.com/openai/v1/chat/completions"
DEFAULT_MODEL = "llama-3.3-70b-versatile"
DEFAULT_MAX_TOKENS = 2000


class GroqGenerator(AnalysisGenerator):

    name = "groq"

    def __init__(self, model: str = DEFAULT_MODEL, max_tokens: int = DEFAULT_MAX_TOKENS):
        self.model = model
        self.max_tokens = max_tokens
        self.client = HttpClient()

    def generate(self, article, prompt_template: str) -> Analysis:
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ProviderUnavailable(
                "GROQ_API_KEY is not set. Get a free key at "
                "https://console.groq.com/keys and export it."
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
                f"Groq HTTP {response.status_code}: {response.body}"
            )

        try:
            payload = json.loads(response.body)
            text = payload["choices"][0]["message"]["content"]
        except (json.JSONDecodeError, KeyError, IndexError, TypeError) as exc:
            raise InvalidProviderResponse(
                f"Could not parse Groq response: {exc}"
            ) from exc

        if not text:
            raise InvalidProviderResponse("Groq response contained no text content.")

        return Analysis(text=text, source_model=self.model)
