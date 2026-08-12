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
        # Braces in the JSON schema are doubled ({{ }}) because this
        # prompt goes through generator.generate(), which calls
        # str.format(title=..., abstract=..., doi=...) on it -- a
        # single-brace JSON example here would collide with str.format.
        prompt = (
            "You are an independent scientific evaluator. "
            "Your task is to compare RAW and BSI analyses fairly and "
            "scientifically.\\n\\n"

            "IMPORTANT INDEPENDENCE RULES:\\n"
            "1. Do not assume that RAW is superior merely because it is "
            "simpler or does not use a specialized analytical framework.\\n"
            "2. Do not assume that BSI is superior merely because it uses "
            "a specialized framework.\\n"
            "3. You may consider BSI-specific analytical capabilities "
            "when they are relevant to the scientific task and the article. "
            "Do NOT automatically exclude, ignore, or penalize capabilities "
            "simply because they originate from BSI.\\n"
            "4. You are NOT required to use BSI's internal vocabulary "
            "(such as D1-D7 or EIG), but you are permitted to recognize "
            "and evaluate the underlying analytical capabilities they "
            "represent when those capabilities are observable in the BSI "
            "analysis. Translate them into scientifically meaningful "
            "evaluation criteria rather than treating the vocabulary "
            "itself as evidence of quality.\\n\\n"

            "ARTICLE-ADAPTIVE CRITERIA:\\n"
            "5. Read the article title and both analyses carefully.\\n"
            "6. Develop 4-8 evaluation criteria appropriate to THIS specific "
            "article, its scientific domain, and the task of comparing the "
            "two analyses.\\n"
            "7. Criteria must be substantive and analytically meaningful. "
            "Do not create criteria merely to favor RAW or BSI.\\n"
            "8. Assign an importance weight to EACH criterion yourself. "
            "Weights must reflect the criterion's relative importance for "
            "THIS article, not simply the number of criteria.\\n"
            "9. Use weights from 5 to 35. The weights MUST sum exactly to 100.\\n"
            "10. Do NOT use equal weights by default. At least two criteria "
            "MUST have different weights unless genuinely equal importance "
            "is scientifically justified. If equal weighting is justified, "
            "explain why explicitly.\\n"
            "11. For EVERY criterion, briefly explain why its assigned "
            "weight is appropriate for this particular article.\\n\\n"

            "SCORING:\\n"
            "12. Score RAW and BSI independently on every criterion from "
            "0-10.\\n"
            "13. Base scores on the actual analytical content provided, "
            "not on the name of the framework.\\n"
            "14. Do not award a bonus or penalty merely because an analysis "
            "uses or does not use BSI.\\n\\n"

            "BSI CAPABILITY ASSESSMENT:\\n"
            "15. Separately assess BSI's capability relevance: whether "
            "the capabilities represented by BSI are relevant to this "
            "article and analytical task.\\n"
            "16. Separately assess capability realization: whether those "
            "relevant capabilities were actually realized effectively in "
            "the BSI analysis supplied here.\\n"
            "17. Separately assess incremental value: whether BSI provides "
            "analytical value beyond RAW. This may be high, medium, low, "
            "none, or negative.\\n"
            "18. These BSI assessments must NEVER constitute an automatic "
            "bonus to the BSI score.\\n\\n"

            "FINAL DECISION:\\n"
            "19. Give an overall winner (raw/bsi/tie) for analytical quality.\\n"
            "20. Give a concise overall reason supported by the actual "
            "comparison.\\n\\n"

            "Return ONLY valid JSON, exactly this shape:\\n"
            '{{"criteria":[{{"name":"","importance":20,"raw_score":0,'
            '"bsi_score":0,"reason":""}}],'
            '"bsi_capability_assessment":{{'
            '"relevance":"high|medium|low",'
            '"realization":"high|medium|low",'
            '"incremental_value":"high|medium|low|none|negative",'
            '"reason":""}},'
            '"winner":"raw|bsi|tie",'
            '"incremental_value":"high|medium|low|none|negative",'
            '"reasoning":""}}\\n\\n'

            f"ARTICLE TITLE\\n{article.title}\\n\\n"
            f"RAW ANALYSIS\\n{raw_text}\\n\\n"
            f"BSI ANALYSIS\\n{bsi_text}\\n"
        )

        result = self.generator.generate(article, prompt)
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

        if abs(weight_sum - 100.0) > 0.01:
            raise ValueError(
                f"LLM judge weights must sum to exactly 100; got {weight_sum}"
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

        weight_sum = round(sum(c["importance"] for c in criteria), 2)
        raw_total = round(sum(c["raw_score"] * c["importance"] for c in criteria) / weight_sum, 2)
        bsi_total = round(sum(c["bsi_score"] * c["importance"] for c in criteria) / weight_sum, 2)

        return {
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
