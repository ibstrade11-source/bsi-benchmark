"""
LLMJudge compares RAW and BSI analyses using an independent LLM judge.

The judge develops article-appropriate evaluation criteria and scores both
analyses fairly. It is not required to use BSI's internal vocabulary
(such as D1-D7 or EIG), but it may recognize and evaluate the underlying
BSI capabilities when they are scientifically relevant and observable in
the supplied BSI analysis.

If no generator is available, or the LLM call/response parsing fails,
the judge falls back to a simple keyword-presence heuristic. The returned
result always identifies the actual evaluation path through
criteria_source ("llm" or "heuristic_fallback").
"""

import json

from bsi_benchmark.comparison.glossary import load_judge_resource, load_compact_glossary
class LLMJudge:

    @staticmethod
    def _extract_json(text):
        """Extract a JSON object from an LLM response.

        Provider-agnostic: works with plain JSON, markdown fences,
        or explanatory text surrounding a JSON object.
        """
        text = (text or "").strip()

        if not text:
            raise ValueError("LLM judge returned an empty response")

        # Direct JSON first.
        try:
            return json.loads(text)
        except (json.JSONDecodeError, ValueError):
            pass

        # Remove markdown fences if present.
        if "```" in text:
            parts = text.split("```")
            for part in parts:
                candidate = part.strip()
                if candidate.startswith("json"):
                    candidate = candidate[4:].lstrip()
                if not candidate:
                    continue
                try:
                    return json.loads(candidate)
                except (json.JSONDecodeError, ValueError):
                    pass

        # Find the outermost JSON object.
        start = text.find("{")
        if start >= 0:
            depth = 0
            in_string = False
            escaped = False

            for i in range(start, len(text)):
                ch = text[i]

                if in_string:
                    if escaped:
                        escaped = False
                    elif ch == "\\":
                        escaped = True
                    elif ch == '"':
                        in_string = False
                    continue

                if ch == '"':
                    in_string = True
                elif ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                    if depth == 0:
                        candidate = text[start:i + 1]
                        try:
                            return json.loads(candidate)
                        except (json.JSONDecodeError, ValueError):
                            break

        raise ValueError(
            "LLM judge response did not contain a valid JSON object"
        )


    SUGGESTED = [
        ("structural_layers", 30),
        ("epistemic_separation", 20),
        ("uncertainty_awareness", 20),
        ("evidence_grounding", 15),
        ("analysis_depth", 15),
    ]

    def __init__(self, generator=None):
        self.generator = generator

    def compare(self, article, raw_analysis, bsi_analysis):
        raw_text = raw_analysis.text if raw_analysis else ""
        bsi_text = bsi_analysis.text if bsi_analysis else ""

        if self.generator is not None:
            try:
                return self._compare_with_llm(article, raw_text, bsi_text)
            except Exception as e:
                print("JUDGE_LLM_ERROR:", repr(e))

                # Preserve the existing fallback behavior for self-judge
                # and explicit judge modes, but expose the real failure
                # so it can be diagnosed from the benchmark result.
                fallback = self._compare_with_heuristic(raw_text, bsi_text)
                fallback["judge_error"] = repr(e)
                fallback["judge_failure_stage"] = "llm_compare"
                return fallback

        return self._compare_with_heuristic(raw_text, bsi_text)

    def _compare_with_llm(self, article, raw_text, bsi_text):
        # Architecture:
        # - system_prompt contains judging instructions only.
        # - user_prompt contains the actual RAW/BSI comparison task.
        # - judge_resource contains independent judge-side knowledge.
        #
        # The glossary is therefore NOT part of the comparison prompt.
        # Provider implementations are responsible for transporting the
        # judge resource through the explicit judge-resource API.
        #
        # The glossary is a judge-side RESOURCE, not part of the
        # comparison prompt. Keep the two concepts architecturally separate.
        full_resource = load_judge_resource()
        compact_resource = load_compact_glossary(max_chars=3500)

        if not full_resource and not compact_resource:
            raise RuntimeError(
                "BSI Judge requires the glossary judge resource, but "
                "docs/BSI_GLOSSARY_FINAL.md could not be loaded "
                "or BSI_JUDGE_GLOSSARY is disabled"
            )

        system_prompt = (
            "You are an independent scientific evaluator comparing RAW and BSI fairly. "
            "Your task is to compare RAW and BSI analyses fairly and "
            "scientifically.\n\n"
            "INDEPENDENCE RULES:\n"
            "Evaluate RAW and BSI impartially. Judge actual capabilities, "
            "not framework labels; no automatic reward or penalty.\n\n"

            "ARTICLE-ADAPTIVE CRITERIA:\n"
            "Create 4-8 substantive article-specific criteria. Weight each "
            "5-35; weights must sum to 100. Avoid equal weights unless "
            "scientifically justified; briefly justify every weight.\n\n"
            "SCORING:\n"
            "Score RAW and BSI independently from 0-10 using actual "
            "content; no automatic BSI bonus or penalty.\n\n"
            "BSI CAPABILITY ASSESSMENT:\n"
            "Separately rate BSI relevance, realization, and incremental "
            "value beyond RAW. Base relevance/realization on this article "
            "and the supplied BSI analysis. These ratings never create an "
            "automatic BSI score bonus.\n\n"
            "FINAL DECISION:\n"
            "Choose raw, bsi, or tie and give a concise evidence-grounded "
            "reason.\n\n"
            "Return ONLY valid JSON with this shape:\n"
            '{"criteria":[{"name":"","importance":20,"raw_score":0,'
            '"bsi_score":0,"reason":""}],'
            '"bsi_capability_assessment":{"relevance":"high|medium|low",'
            '"realization":"high|medium|low",'
            '"incremental_value":"high|medium|low|none|negative",'
            '"reason":""},"winner":"raw|bsi|tie",'
            '"incremental_value":"high|medium|low|none|negative",'
            '"reasoning":""}\n\n'
            "The article title and the two analyses to compare follow in "
            "the next message."
        )

        user_prompt = (
            f"ARTICLE TITLE\n{article.title}\n\n"
            f"RAW ANALYSIS\n{raw_text}\n\n"
            f"BSI ANALYSIS\n{bsi_text}\n"
        )

        def _is_token_limit_error(exc):
            msg = str(exc).lower()
            keys = (
                "413",
                "request too large",
                "tokens per minute",
                "tpm",
                "rate_limit_exceeded",
                "context length",
                "maximum context",
                "too many tokens",
                "token limit",
            )
            return any(k in msg for k in keys)

        # Prefer full glossary; only fall back to compact on token-limit errors.
        last_error = None
        result = None
        used_compact = False

        for resource, is_compact in (
            (full_resource, False),
            (compact_resource, True),
        ):
            if not resource:
                continue
            try:
                result = self.generator.generate_with_judge_resource(
                    article, system_prompt, user_prompt, resource
                )
                used_compact = is_compact
                break
            except Exception as e:
                last_error = e
                if is_compact or not _is_token_limit_error(e):
                    raise
                print("JUDGE_TOKEN_LIMIT: retrying with compact glossary")

        if result is None:
            raise last_error if last_error else RuntimeError("Judge generation failed")

        text = (result.text or "").strip()

        if text.startswith("```"):
            lines = text.splitlines()[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            text = "\n".join(lines)

        # Groq may occasionally wrap an otherwise valid JSON object
        # in explanatory prose or markdown fences. Extract the JSON
        # object before giving up and falling back to the heuristic.
        try:
            parsed = self._extract_json(text)
        except (json.JSONDecodeError, ValueError):
            decoder = json.JSONDecoder()
            parsed = None

            # Try every opening brace until a complete JSON object is found.
            for start in (i for i, ch in enumerate(text) if ch == "{"):
                try:
                    candidate, end = decoder.raw_decode(text[start:])
                    if isinstance(candidate, dict):
                        parsed = candidate
                        break
                except (json.JSONDecodeError, ValueError):
                    continue

            if parsed is None:
                raise ValueError(
                    "LLM judge response did not contain a parseable JSON object"
                )

        raw_criteria = parsed.get("criteria", [])
        if not raw_criteria:
            raise ValueError("LLM judge returned no criteria")

        if not 4 <= len(raw_criteria) <= 8:
            raise ValueError(
                f"LLM judge returned {len(raw_criteria)} criteria; expected 4-8"
            )

        capability = parsed.get("bsi_capability_assessment", {})
        if not isinstance(capability, dict):
            raise ValueError(
                "LLM judge returned an invalid bsi_capability_assessment object"
            )

        allowed_relevance = {"high", "medium", "low"}
        allowed_incremental = {"high", "medium", "low", "none", "negative"}

        relevance = str(capability.get("relevance", "")).strip().lower()
        realization = str(capability.get("realization", "")).strip().lower()
        capability_incremental = str(
            capability.get("incremental_value", "")
        ).strip().lower()
        top_incremental = str(
            parsed.get("incremental_value", "")
        ).strip().lower()

        if relevance not in allowed_relevance:
            raise ValueError(
                "LLM judge returned invalid BSI capability relevance: "
                f"{relevance!r}"
            )

        if realization not in allowed_relevance:
            raise ValueError(
                "LLM judge returned invalid BSI capability realization: "
                f"{realization!r}"
            )

        if capability_incremental not in allowed_incremental:
            raise ValueError(
                "LLM judge returned invalid BSI capability incremental_value: "
                f"{capability_incremental!r}"
            )

        if top_incremental not in allowed_incremental:
            raise ValueError(
                "LLM judge returned invalid top-level incremental_value: "
                f"{top_incremental!r}"
            )

        if capability_incremental != top_incremental:
            raise ValueError(
                "LLM judge returned inconsistent incremental_value values "
                "between bsi_capability_assessment and the top-level field"
            )

        capability = {
            "relevance": relevance,
            "realization": realization,
            "incremental_value": capability_incremental,
            "reason": str(capability.get("reason", "")).strip(),
        }

        criteria = []
        for item in raw_criteria:
            name = str(item.get("name", "")).strip()
            reason = str(item.get("reason", "")).strip()

            if not name:
                raise ValueError("LLM judge returned a criterion without a name")

            try:
                importance = float(item.get("importance"))
                raw_score = float(item.get("raw_score"))
                bsi_score = float(item.get("bsi_score"))
            except (TypeError, ValueError):
                raise ValueError("LLM judge returned a non-numeric weight or score")

            if not 5 <= importance <= 35:
                raise ValueError(
                    f"Criterion '{name}' has invalid importance {importance}; "
                    "expected 5-35"
                )

            if not 0 <= raw_score <= 10 or not 0 <= bsi_score <= 10:
                raise ValueError(
                    f"Criterion '{name}' has score outside 0-10"
                )

            criteria.append(
                {
                    "name": name,
                    "importance": importance,
                    "raw_score": raw_score,
                    "bsi_score": bsi_score,
                    "reason": reason,
                }
            )

        weight_sum = sum(c["importance"] for c in criteria)

        if weight_sum <= 0:
            raise ValueError(
                f"LLM judge returned invalid total importance weight: {weight_sum}"
            )

        if abs(weight_sum - 100.0) > 0.01:
            # LLMs may occasionally return valid per-criterion weights
            # whose total is slightly or substantially different from 100.
            # Normalize rather than discarding an otherwise usable judgment.
            for c in criteria:
                c["importance"] = (
                    float(c["importance"]) * 100.0 / weight_sum
                )

            # Remove floating-point drift so the total is exactly 100.
            corrected_sum = sum(c["importance"] for c in criteria)
            drift = 100.0 - corrected_sum

            largest = max(
                criteria,
                key=lambda c: float(c["importance"])
            )
            largest["importance"] = (
                float(largest["importance"]) + drift
            )

        weight_sum = sum(c["importance"] for c in criteria)

        if abs(weight_sum - 100.0) > 0.01:
            raise ValueError(
                f"LLM judge weight repair failed; got {weight_sum}"
            )

        distinct_weights = {
            round(c["importance"], 4) for c in criteria
        }

        if len(distinct_weights) == 1:
            if not all(c["reason"].strip() for c in criteria):
                raise ValueError(
                    "LLM judge used equal weights for every criterion "
                    "without providing a scientific justification for "
                    "the equal weighting"
                )

        for c in criteria:
            c["importance"] = round(c["importance"], 2)

        # Correct rounding drift after normalizing weights.
        weight_sum = round(sum(c["importance"] for c in criteria), 2)
        if weight_sum != 100.0:
            drift = round(100.0 - weight_sum, 2)
            largest = max(
                criteria,
                key=lambda c: float(c["importance"])
            )
            largest["importance"] = round(
                float(largest["importance"]) + drift,
                2
            )

        weight_sum = round(sum(c["importance"] for c in criteria), 2)

        if weight_sum != 100.0:
            raise ValueError(
                f"LLM judge final weight repair failed; got {weight_sum}"
            )

        raw_total = round(sum(c["raw_score"] * c["importance"] for c in criteria) / weight_sum, 2)
        bsi_total = round(sum(c["bsi_score"] * c["importance"] for c in criteria) / weight_sum, 2)

        out = {
            "criteria_source": "llm",
            "winner": parsed.get("winner", "bsi" if bsi_total > raw_total else "raw"),
            "reasoning": parsed.get("reasoning", ""),
            "criteria": criteria,
            "total_scores": {"raw": raw_total, "bsi": bsi_total},
            "bsi_capability_assessment": capability,
            "incremental_value": capability["incremental_value"],
            "scale": "0-10",
            "weight_sum": round(weight_sum, 1),
        }
        if used_compact:
            out["glossary_mode"] = "compact_fallback"
        else:
            out["glossary_mode"] = "full"
        return out

    def _compare_with_heuristic(self, raw, bsi):
        def has(txt, *keys):
            txt = txt.lower()
            return any(k.lower() in txt for k in keys)

        rl = 10 if has(raw, "manifest") else 0
        bl = 10 if has(bsi, "manifest", "latent", "meta") else 0
        re_ = 10 if has(raw, "fact", "inference", "speculation") else 0
        be = 10 if has(bsi, "fact", "inference", "speculation") else 0
        ru = 10 if has(raw, "uncertain", "may", "might", "assumption") else 2
        bu = 10 if has(bsi, "uncertain", "may", "might", "assumption") else 2
        rg, bg = 6, 8
        rd = min(10, max(1, len(raw) // 120))
        bd = min(10, max(1, len(bsi) // 120))

        values = [
            ("structural_layers", 30, rl, bl, "Presence of analytical layers"),
            ("epistemic_separation", 20, re_, be, "Fact / inference / speculation separation"),
            ("uncertainty_awareness", 20, ru, bu, "Recognition of uncertainty"),
            ("evidence_grounding", 15, rg, bg, "Grounding in evidence"),
            ("analysis_depth", 15, rd, bd, "Analytical coverage"),
        ]

        criteria = []
        raw_total = bsi_total = 0.0
        for name, w, rs, bs, reason in values:
            raw_total += rs * w
            bsi_total += bs * w
            criteria.append({"name": name, "importance": w, "raw_score": rs, "bsi_score": bs, "reason": reason})

        raw_total = round(raw_total / 100, 2)
        bsi_total = round(bsi_total / 100, 2)

        return {
            "criteria_source": "heuristic_fallback",
            "winner": "bsi" if bsi_total > raw_total else "raw",
            "reasoning": (
                "No LLM judge was available or its response could not be "
                "parsed -- this result is from a fixed keyword-presence "
                "heuristic, not an independent LLM judgement. Treat it as "
                "a placeholder, not a real evaluation."
            ),
            "criteria": criteria,
            "total_scores": {"raw": raw_total, "bsi": bsi_total},
            "bsi_capability_assessment": {
                "relevance": "low",
                "realization": "low",
                "incremental_value": "none",
                "reason": (
                    "Heuristic fallback cannot validly assess BSI capability "
                    "relevance, realization, or incremental value."
                ),
            },
            "incremental_value": "none",
            "scale": "0-10",
            "weight_sum": 100,
        }
