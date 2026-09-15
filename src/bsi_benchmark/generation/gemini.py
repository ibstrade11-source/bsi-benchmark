"""
GeminiGenerator: calls the Google AI Studio (Gemini) generateContent API.

Requires the GEMINI_API_KEY environment variable. Never hardcode a key in
this file or in configs/ -- read it from the environment only, so keys
never end up committed to the repo.
"""

import json
import os
import time

from bsi_benchmark.network import HttpClient
from bsi_benchmark.models.analysis import Analysis
from bsi_benchmark.errors import ProviderUnavailable, InvalidProviderResponse

from .base import AnalysisGenerator
from .prompt import render

API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
GEMINI_MAX_RETRIES = int(os.getenv("GEMINI_MAX_RETRIES", "50"))
GEMINI_RETRY_DELAY = float(os.getenv("GEMINI_RETRY_DELAY", "5"))


class GeminiGenerator(AnalysisGenerator):

    name = "gemini"

    def __init__(self, model: str = DEFAULT_MODEL):
        self.model = model
        self.client = HttpClient()

    def _api_key(self) -> str:
        api_key = (
            os.environ.get("GEMINI_API_KEY", "")
            .strip()
            .encode("ascii", "ignore")
            .decode("ascii")
        )
        if not api_key:
            raise ProviderUnavailable(
                "GEMINI_API_KEY is not set. Get a free key at "
                "https://aistudio.google.com/apikey and export it."
            )
        return api_key

    def _post(self, payload):
        url = f"{API_BASE}/{self.model}:generateContent"
        api_key = self._api_key()

        for attempt in range(GEMINI_MAX_RETRIES + 1):
            response = self.client.post(
                url,
                json_body=payload,
                headers={
                    "x-goog-api-key": api_key,
                    "content-type": "application/json",
                },
            )

            if response.ok:
                return response

            if response.status_code == 503 and attempt < GEMINI_MAX_RETRIES:
                print(
                    f"[gemini] HTTP 503 (high demand). "
                    f"Retry {attempt + 1}/{GEMINI_MAX_RETRIES} "
                    f"in {GEMINI_RETRY_DELAY:g}s...",
                    flush=True,
                )
                time.sleep(GEMINI_RETRY_DELAY)
                continue

            if response.status_code == 503:
                raise ProviderUnavailable(
                    f"Gemini HTTP 503 after {GEMINI_MAX_RETRIES} retries: "
                    f"{response.body}"
                )

            if response.status_code == 429:
                body = str(response.body)
                body_lower = body.lower()

                quota_or_tpm = any(
                    marker in body_lower
                    for marker in (
                        "quota",
                        "tpm",
                        "tokens per minute",
                        "token per minute",
                        "prompt too long",
                        "prompt length",
                        "input token",
                        "input tokens",
                        "exceeded your current quota",
                    )
                )

                if quota_or_tpm:
                    raise ProviderUnavailable(
                        "Gemini HTTP 429 — NO RETRY. "
                        "The request appears to have hit a quota/TPM/"
                        "prompt-length limit. DO NOT run manual RETRY & RESUME "
                        "for this cell; resubmitting the same request is not "
                        "expected to help and may consume additional quota. "
                        f"Response: {body}"
                    )

                raise ProviderUnavailable(
                    "Gemini HTTP 429 — NO RETRY. "
                    "Do not run manual RETRY & RESUME unless the request/"
                    "provider limit has materially changed. "
                    f"Response: {body}"
                )


            raise ProviderUnavailable(
                f"Gemini HTTP {response.status_code}: {response.body}"
            )

    @staticmethod
    def _extract_text(response) -> str:
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
            finish_reason = (
                candidates[0].get("finishReason")
                if candidates
                else None
            )

            raise InvalidProviderResponse(
                "Gemini response contained no text content"
                + (
                    f" (finishReason={finish_reason})"
                    if finish_reason
                    else "."
                )
            )

        return text

    def generate(self, article, prompt_template: str) -> Analysis:
        prompt = render(prompt_template, article)

        response = self._post(
            {
                "contents": [
                    {
                        "parts": [
                            {"text": prompt}
                        ]
                    }
                ]
            }
        )

        text = self._extract_text(response)

        return Analysis(
            text=text,
            source_model=self.model,
        )

    def generate_with_judge_resource(
        self,
        article,
        system_prompt: str,
        user_prompt: str,
        judge_resource: str | None = None,
    ) -> Analysis:
        """Transport a provider-neutral independent judge request.

        The prompt construction remains in the Judge layer. This method only
        maps the already-separated system prompt, user prompt, and optional
        independent judge resource onto Gemini's native API fields.

        The judge resource is transported through Gemini's
        system_instruction channel and is never appended to the comparison
        user prompt.
        """
        system_text = system_prompt

        if judge_resource:
            system_text = (
                f"{system_prompt}\n\n"
                "INDEPENDENT JUDGE RESOURCE\n"
                f"{judge_resource}"
            )

        payload = {
            "system_instruction": {
                "parts": [
                    {"text": system_text}
                ]
            },
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {"text": user_prompt}
                    ]
                }
            ],
        }

        response = self._post(payload)
        text = self._extract_text(response)

        return Analysis(
            text=text,
            source_model=self.model,
        )
