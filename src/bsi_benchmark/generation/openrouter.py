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

        return self._call_messages(
            api_key, [{"role": "user", "content": prompt}]
        )

    def generate_with_system(self, article, system_prompt: str, user_prompt: str) -> Analysis:
        api_key = os.environ.get('OPENROUTER_API_KEY')
        if not api_key:
            raise ProviderUnavailable(
                "OPENROUTER_API_KEY is not set."
            )
        return self._call_messages(
            api_key,
            [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )

    def _call_messages(self, api_key: str, messages: list) -> Analysis:
        response = self.client.post(
            API_URL,
            json_body={
                "model": self.model,
                "max_tokens": self.max_tokens,
                "messages": messages,
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
        except json.JSONDecodeError as exc:
            raise InvalidProviderResponse(
                "OpenRouter returned HTTP 200 but the response body was not "
                f"valid JSON: {exc}. Body prefix={response.body[:1000]!r}"
            ) from exc

        if not isinstance(payload, dict):
            raise InvalidProviderResponse(
                "OpenRouter returned an unexpected JSON type: "
                f"{type(payload).__name__}"
            )

        # OpenRouter normally returns the OpenAI-compatible:
        # choices[0].message.content
        # If that structure is absent, preserve enough response information
        # to diagnose provider/model failures instead of exposing only
        # a cryptic KeyError such as "'choices'".
        choices = payload.get("choices")

        if not isinstance(choices, list) or not choices:
            error = payload.get("error")
            raise InvalidProviderResponse(
                "OpenRouter response did not contain a non-empty 'choices' "
                f"array. keys={list(payload.keys())!r}; "
                f"error={error!r}; body_prefix={response.body[:1500]!r}"
            )

        first = choices[0]
        if not isinstance(first, dict):
            raise InvalidProviderResponse(
                "OpenRouter response contained an invalid first choice: "
                f"{first!r}"
            )

        message = first.get("message")
        if not isinstance(message, dict):
            raise InvalidProviderResponse(
                "OpenRouter response choice did not contain a valid "
                f"'message' object: {first!r}"
            )

        text = message.get("content")

        if not isinstance(text, str):
            raise InvalidProviderResponse(
                "OpenRouter response message did not contain string "
                f"'content'. message_keys={list(message.keys())!r}"
            )

        if not text.strip():
            raise InvalidProviderResponse(
                "OpenRouter response contained empty text content."
            )

        return Analysis(text=text, source_model=self.model)
