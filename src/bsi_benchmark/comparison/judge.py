"""
LLMJudge: sends both analyses to an LLM and asks it to independently
choose its own evaluation criteria (never BSI's own D1-D7/EIG vocabulary)
and score both analyses against them.

If no generator is available, or the LLM call/response-parsing fails for
any reason, falls back to a simple keyword-presence heuristic -- but the
returned result always says honestly which path produced it
(criteria_source: "llm" or "heuristic_fallback"), never both at once.
"""
import json


class LLMJudge:

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
            except Exception:
                pass  # fall through to the honestly-labeled heuristic below

        return self._compare_with_heuristic(raw_text, bsi_text)

    def _compare_with_llm(self, article, raw_text, bsi_text):
        # Braces in the JSON schema are doubled ({{ }}) because this
        # prompt goes through generator.generate(), which calls
        # str.format(title=..., abstract=..., doi=...) on it -- a
        # single-brace JSON example here would collide with str.format.
        prompt = (
            "You are an independent scientific evaluator. Do NOT use "
            "BSI's own scoring system (D1-D7, EIG, Manifest/Latent/Meta, "
            "FACT/INFERENCE tags) as your criteria -- choose your own, "
            "in your own judgement.\n\n"
            "1. Read the article title.\n"
            "2. Read BOTH analyses below.\n"
            "3. Invent your own 4-8 evaluation criteria.\n"
            "4. Score RAW and BSI on each, 0-10.\n"
            "5. Give an overall winner (raw/bsi/tie) and a short reason.\n\n"
            "Return ONLY valid JSON, exactly this shape:\n"
            '{{"criteria":[{{"name":"","raw_score":0,"bsi_score":0,'
            '"reason":""}}],"winner":"raw|bsi|tie","reasoning":""}}\n\n'
            f"ARTICLE TITLE\n{article.title}\n\n"
            f"RAW ANALYSIS\n{raw_text}\n\n"
            f"BSI ANALYSIS\n{bsi_text}\n"
        )

        result = self.generator.generate(article, prompt)
        text = (result.text or "").strip()

        if text.startswith("```"):
            lines = text.splitlines()[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            text = "\n".join(lines)

        parsed = json.loads(text)
        raw_criteria = parsed.get("criteria", [])
        if not raw_criteria:
            raise ValueError("LLM judge returned no criteria")

        weight = round(100 / len(raw_criteria), 1)
        criteria = [
            {
                "name": item.get("name", ""),
                "importance": weight,
                "raw_score": float(item.get("raw_score", 0)),
                "bsi_score": float(item.get("bsi_score", 0)),
                "reason": item.get("reason", ""),
            }
            for item in raw_criteria
        ]

        weight_sum = sum(c["importance"] for c in criteria)
        raw_total = round(sum(c["raw_score"] * c["importance"] for c in criteria) / weight_sum, 2)
        bsi_total = round(sum(c["bsi_score"] * c["importance"] for c in criteria) / weight_sum, 2)

        return {
            "criteria_source": "llm",
            "winner": parsed.get("winner", "bsi" if bsi_total > raw_total else "raw"),
            "reasoning": parsed.get("reasoning", ""),
            "criteria": criteria,
            "total_scores": {"raw": raw_total, "bsi": bsi_total},
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
            "scale": "0-10",
            "weight_sum": 100,
        }
