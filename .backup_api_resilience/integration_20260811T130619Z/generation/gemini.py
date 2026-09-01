"""
GeminiGenerator: calls the Google AI Studio (Gemini) generateContent API.

Requires the GEMINI_API_KEY environment variable. Never hardcode a key in
this file or in configs/ -- read it from the environment only, so keys
never end up committed to the repo.
"""

import json
import os

from bsi_benchmark.network import HttpClient
from bsi_benchmark.models.analysis import Analysis
from bsi_benchmark.errors import ProviderUnavailable, InvalidProviderResponse

from .base import AnalysisGenerator
from .prompt import render

API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"
DEFAULT_MODEL = "gemini-3.5-flash"


class GeminiGenerator(AnalysisGenerator):

    name = "gemini"

    def __init__(self, model: str = DEFAULT_MODEL):
        self.model = model
        self.client = HttpClient()

    def generate(self, article, prompt_template: str) -> Analysis:
        api_key = os.environ.get("GEMINI_API_KEY", "").strip().encode("ascii", "ignore").decode("ascii")
        if not api_key:
            raise ProviderUnavailable(
                "GEMINI_API_KEY is not set. Get a free key at "
                "https://aistudio.google.com/apikey and export it."
            )

        prompt = render(prompt_template, article)
        url = f"{API_BASE}/{self.model}:generateContent"

        response = self.client.post(
            url,
            json_body={"contents": [{"parts": [{"text": prompt}]}]},
            headers={
                "x-goog-api-key": api_key,
                "content-type": "application/json",
            },
        )

        if not response.ok:
            raise ProviderUnavailable(
                f"Gemini HTTP {response.status_code}: {response.body}"
            )

        try:
            payload = json.loads(response.body)
            candidates = payload.get("candidates") or []
            text = "".join(
                part.get("text", "")
                for candidate in candidates
                for part in candidate.get("content", {}).get("parts", [])
            )
        except (json.JSONDecodeError, AttributeError, TypeError) as exc:
            raise InvalidProviderResponse(
                f"Could not parse Gemini response: {exc}"
            ) from exc

        if not text:
            finish_reason = candidates[0].get("finishReason") if candidates else None
            raise InvalidProviderResponse(
                "Gemini response contained no text content"
                + (f" (finishReason={finish_reason})" if finish_reason else ".")
            )

        return Analysis(text=text, source_model=self.model)
