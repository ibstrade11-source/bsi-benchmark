"""
AnthropicGenerator: calls the Anthropic Messages API.

Requires the ANTHROPIC_API_KEY environment variable. Never hardcode a key
in this file or in configs/ -- read it from the environment only, so keys
never end up committed to the repo.
"""

import json
import os

from bsi_benchmark.network import HttpClient
from bsi_benchmark.models.analysis import Analysis
from bsi_benchmark.errors import ProviderUnavailable, InvalidProviderResponse

from .base import AnalysisGenerator
from .prompt import render

API_URL = "https://api.anthropic.com/v1/messages"
API_VERSION = "2023-06-01"
DEFAULT_MODEL = "claude-sonnet-5"
DEFAULT_MAX_TOKENS = 2000


class AnthropicGenerator(AnalysisGenerator):

    name = "anthropic"

    def __init__(self, model: str = DEFAULT_MODEL, max_tokens: int = DEFAULT_MAX_TOKENS):
        self.model = model
        self.max_tokens = max_tokens
        self.client = HttpClient()

    def generate(self, article, prompt_template: str) -> Analysis:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ProviderUnavailable(
                "ANTHROPIC_API_KEY is not set. Export it before running "
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
                "x-api-key": api_key,
                "anthropic-version": API_VERSION,
                "content-type": "application/json",
            },
        )

        if not response.ok:
            raise ProviderUnavailable(
                f"Anthropic HTTP {response.status_code}: {response.body}"
            )

        try:
            payload = json.loads(response.body)
            text = "".join(
                block.get("text", "")
                for block in payload.get("content", [])
                if block.get("type") == "text"
            )
        except (json.JSONDecodeError, AttributeError, TypeError) as exc:
            raise InvalidProviderResponse(
                f"Could not parse Anthropic response: {exc}"
            ) from exc

        if not text:
            raise InvalidProviderResponse(
                "Anthropic response contained no text content."
            )

        return Analysis(text=text, source_model=self.model)
