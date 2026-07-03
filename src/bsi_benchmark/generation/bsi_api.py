"""
BSIAPIGenerator: calls Ma's own deployed BSI API (the six-stage
BSI->EIG->ECC->DRAFT->REIG->FINAL SYNTHESIS pipeline from the main
behmanesh-index-prompt repository) instead of a raw chat-completion API.

NOTE: the exact request/response JSON shape below is a best-effort
reconstruction from memory -- it has NOT been verified against the real
docs/openapi.yaml or api/routes/bsi.py source. Update _CANDIDATE_TEXT_FIELDS
and the request body once the real schema is confirmed.
"""

import json
import os

from bsi_benchmark.network import HttpClient
from bsi_benchmark.models.analysis import Analysis
from bsi_benchmark.errors import ProviderUnavailable, InvalidProviderResponse

from .base import AnalysisGenerator

DEFAULT_BASE_URL = "https://behmanesh-index-prompt-production.up.railway.app"

_CANDIDATE_TEXT_FIELDS = [
    "final_synthesis",
    "synthesis",
    "draft",
    "result",
    "analysis",
    "output",
    "text",
]


class BSIAPIGenerator(AnalysisGenerator):

    name = "bsi_api"

    def __init__(self, base_url: str | None = None, endpoint: str = "/bsi/analyze", detail: bool = True):
        self.base_url = (
            base_url
            or os.environ.get("BSI_API_URL")
            or DEFAULT_BASE_URL
        ).rstrip("/")
        self.endpoint = endpoint
        self.detail = detail
        self.client = HttpClient()

    def generate(self, article, prompt_template: str) -> Analysis:
        text_to_analyze = f"{article.title}\n\n{article.abstract or ''}".strip()

        url = f"{self.base_url}{self.endpoint}"

        response = self.client.post(
            url,
            json_body={
                "text": text_to_analyze,
                "detail": self.detail,
            },
            headers={"Content-Type": "application/json"},
        )

        if not response.ok:
            raise ProviderUnavailable(
                f"BSI API HTTP {response.status_code}: {response.body}"
            )

        try:
            payload = json.loads(response.body)
        except json.JSONDecodeError as exc:
            raise InvalidProviderResponse(
                f"Could not parse BSI API response as JSON: {exc}"
            ) from exc

        text = self._extract_text(payload)

        if not text:
            raise InvalidProviderResponse(
                "BSI API response did not contain a recognized text field. "
                f"Response keys were: {list(payload.keys())}. "
                "Update _CANDIDATE_TEXT_FIELDS in bsi_api.py to match the "
                "real response schema."
            )

        return Analysis(text=text, source_model="bsi-api-v3.4.2")

    @staticmethod
    def _extract_text(payload: dict) -> str | None:
        for field in _CANDIDATE_TEXT_FIELDS:
            value = payload.get(field)
            if isinstance(value, str) and value.strip():
                return value
            if isinstance(value, dict):
                for sub_field in _CANDIDATE_TEXT_FIELDS:
                    sub_value = value.get(sub_field)
                    if isinstance(sub_value, str) and sub_value.strip():
                        return sub_value
        return None
