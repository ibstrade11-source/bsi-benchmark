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

# OPENROUTER_MAX_TOKENS lets a real generation run be given more
# headroom without a code change, mirroring the existing
# OPENROUTER_MODEL override pattern.
DEFAULT_MAX_TOKENS = int(os.environ.get("OPENROUTER_MAX_TOKENS", "2000"))

# METHODOLOGY.md section 33 ("Context Limit and Truncation") requires
# that when an output is cut short by a length limit, this be handled
# by a specified, recorded method rather than silently accepted as
# complete. When a response's `finish_reason` is "length" (the
# provider's own signal that max_tokens was hit, not a rate-limit or
# TPM error), up to this many additional "continue where you left off"
# calls are made and concatenated onto the text before giving up. This
# is a distinct mechanism from the token-BUDGET escalation in
# comparison/runner.py (which shrinks an oversized INPUT after a
# rate-limit error); this one extends an undersized OUTPUT after a
# length cutoff, and is opt-in per call (see `allow_continuation` on
# _call_messages) so the judge's short, compact-JSON responses never
# trigger it.
_MAX_CONTINUATION_ROUNDS = 2
_CONTINUATION_INSTRUCTION = (
    "Continue your previous response exactly from where it was cut "
    "off. Do not repeat any earlier text, do not add a preamble or "
    "summary, and do not restart -- just continue the unfinished text "
    "seamlessly."
)


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

    def generate_with_judge_resource(
        self,
        article,
        system_prompt: str,
        user_prompt: str,
        judge_resource: str | None = None,
    ) -> Analysis:
        """Transport judge resource separately from the comparison prompt.

        Architectural contract:

        - system_prompt = judging instructions ONLY
        - user_prompt = RAW/BSI comparison ONLY
        - judge_resource = independent judge knowledge ONLY
        - provider/model identity remains API metadata only
        """
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            raise ProviderUnavailable(
                "OPENROUTER_API_KEY is not set."
            )

        messages = []

        if judge_resource:
            messages.append(
                {
                    "role": "system",
                    "content": (
                        "JUDGE KNOWLEDGE RESOURCE.\n"
                        "Use this only as background knowledge for semantic "
                        "disambiguation of BSI terminology.\n"
                        "It is NOT evidence, NOT a scoring rubric, and NOT "
                        "proof of any conclusion.\n\n"
                        + judge_resource
                    ),
                }
            )

        messages.append(
            {
                "role": "system",
                "content": system_prompt,
            }
        )

        messages.append(
            {
                "role": "user",
                "content": user_prompt,
            }
        )

        return self._call_messages(api_key, messages, allow_continuation=False)

    def _call_messages(
        self, api_key: str, messages: list, allow_continuation: bool = True
    ) -> Analysis:
        working_messages = list(messages)
        combined_text = ""
        finish_reason = None
        usage = None
        rounds = 0

        while True:
            response = self.client.post(
                API_URL,
                json_body={
                    "model": self.model,
                    "max_tokens": self.max_tokens,
                    "messages": working_messages,
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

            if rounds == 0 and not text.strip():
                raise InvalidProviderResponse(
                    "OpenRouter response contained empty text content."
                )

            combined_text += text
            finish_reason = first.get("finish_reason")

            # OpenRouter's response is OpenAI-compatible and normally
            # includes a "usage" object (prompt_tokens/completion_tokens/
            # total_tokens). Passed through as-is when present, never
            # fabricated when absent -- see METHODOLOGY.md section 32
            # (Execution Burden) and section 63 (data integrity: "missing
            # != zero"). Kept as the LAST round's raw usage rather than a
            # synthesized sum across rounds, since summing provider-
            # specific nested usage structures risks producing a number
            # the provider never actually reported.
            round_usage = payload.get("usage")
            usage = round_usage if isinstance(round_usage, dict) else None

            if (
                not allow_continuation
                or finish_reason != "length"
                or rounds >= _MAX_CONTINUATION_ROUNDS
            ):
                break

            working_messages = working_messages + [
                {"role": "assistant", "content": text},
                {"role": "user", "content": _CONTINUATION_INSTRUCTION},
            ]
            rounds += 1

        return Analysis(
            text=combined_text,
            source_model=self.model,
            usage=usage,
            finish_reason=finish_reason,
            continuation_rounds=rounds,
        )
