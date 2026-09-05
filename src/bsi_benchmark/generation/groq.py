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
DEFAULT_MODEL = os.environ.get(
    "GROQ_MODEL",
    "openai/gpt-oss-20b"
)
# GROQ_MAX_TOKENS lets a real generation run be given more headroom
# without a code change, mirroring the existing GROQ_MODEL override
# pattern. This does NOT affect JUDGE_MAX_TOKENS below -- the judge is
# deliberately kept at a small, fixed budget regardless of this
# variable, since it only ever needs to return a compact JSON object
# (see the JUDGE_MAX_TOKENS patch this constant was introduced by).
DEFAULT_MAX_TOKENS = int(os.environ.get("GROQ_MAX_TOKENS", "8000"))

JUDGE_MAX_TOKENS = 2000

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

        return self._call_messages(
            api_key, [{"role": "user", "content": prompt}]
        )

    def generate_with_system(self, article, system_prompt: str, user_prompt: str) -> Analysis:
        api_key = os.environ.get('GROQ_API_KEY')
        if not api_key:
            raise ProviderUnavailable(
                "GROQ_API_KEY is not set."
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

        IMPORTANT ARCHITECTURAL RULE:

        - system_prompt = judging instructions ONLY
        - user_prompt   = RAW/BSI comparison ONLY
        - judge_resource = independent judge knowledge ONLY

        Provider name and model name are API metadata only. They are
        never inserted into any prompt content.
        """
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ProviderUnavailable(
                "GROQ_API_KEY is not set."
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

        # Judging instructions only.
        messages.append(
            {
                "role": "system",
                "content": system_prompt,
            }
        )

        # Actual comparison task only.
        messages.append(
            {
                "role": "user",
                "content": user_prompt,
            }
        )

        return self._call_messages(api_key, messages, max_tokens=JUDGE_MAX_TOKENS, allow_continuation=False)

    def _call_messages(
        self,
        api_key: str,
        messages: list,
        max_tokens: int | None = None,
        allow_continuation: bool = True,
    ) -> Analysis:
        effective_max_tokens = max_tokens if max_tokens is not None else self.max_tokens
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
                    "max_tokens": effective_max_tokens,
                    "reasoning_effort": "low",
                    "messages": working_messages,
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
                choice = payload["choices"][0]
                text = choice["message"]["content"]
            except (json.JSONDecodeError, KeyError, IndexError, TypeError) as exc:
                raise InvalidProviderResponse(
                    f"Could not parse Groq response: {exc}"
                ) from exc

            if not text and rounds == 0:
                raise InvalidProviderResponse("Groq response contained no text content.")

            combined_text += text or ""
            finish_reason = choice.get("finish_reason")

            # Groq's response is OpenAI-compatible and normally includes a
            # "usage" object (prompt_tokens/completion_tokens/total_tokens).
            # Passed through as-is when present, never fabricated when
            # absent -- see METHODOLOGY.md section 32 (Execution Burden)
            # and section 63 (data integrity: "missing != zero"). Kept as
            # the LAST round's raw usage rather than a synthesized sum
            # across rounds, since summing provider-specific nested usage
            # structures risks producing a number the provider never
            # actually reported.
            round_usage = payload.get("usage") if isinstance(payload, dict) else None
            usage = round_usage if isinstance(round_usage, dict) else None

            if (
                not allow_continuation
                or finish_reason != "length"
                or rounds >= _MAX_CONTINUATION_ROUNDS
            ):
                break

            working_messages = working_messages + [
                {"role": "assistant", "content": text or ""},
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
