# Comparison: The Algorithmic Caricature: Auditing LLM-Generated Political Discourse Across Crisis Events

## Run metadata
- bsi-benchmark version: 0.1.0
- git commit: 302bfb085d5c4201756ec36e02199b9f5c65c9db
- run timestamp (UTC): 2026-08-10T04:56:02Z
- methodology: Scores/judgements come from an independent LLM judge (see comparison/judge.py) instructed not to reuse BSI's own D1-D7/EIG vocabulary and to choose its own evaluation criteria. If no judge model is available or its response cannot be parsed, the run falls back to a simple keyword-presence heuristic -- the stored record's own 'criteria_source' field ('llm' vs 'heuristic_fallback') always says honestly which one produced a given result. Neither path is a validated measurement of analytical quality until checked against independent human judgement on a representative sample.

> BSI prompt source: https://github.com/ibstrade11-source/behmanesh-index-prompt/blob/main/MASTER_PROMPT_BSI_v3.4.2.md

## The Algorithmic Caricature: Auditing LLM-Generated Political Discourse Across Crisis Events

*source:* http://arxiv.org/abs/2605.12452v1

### Judge Evaluation

#### Judge Information

| Field | Value |
|---|---|
| Criteria source | llm |
| Score scale | 0-10 |
| Weight sum | 100.0 |

#### Judge Reasoning

**Winner:** bsi

The BSI analysis offers a more comprehensive, nuanced, and original approach to evaluating AI-generated political discourse, particularly through its population-level auditing framework and the 'Caricature Gap' metric. This provides higher incremental value compared to the RAW analysis.

#### Criteria Selected by Judge

| Criterion | Weight | Raw (/10) | BSI (/10) | Weighted Raw | Weighted BSI | Explanation |
|---|---:|---:|---:|---:|---:|---|
| Methodological Validity | 25 | 8.0 | 9.5 | 2.00 | 2.38 | Both analyses demonstrate strong methodological validity, but BSI's use of a paired corpus and evaluation across 9 crisis events adds depth. |
| Data Richness | 20 | 7.0 | 9.5 | 1.40 | 1.90 | BSI's analysis benefits from a richer dataset, including real-world social platform data paired with generated synthetic counterparts. |
| Theoretical Coherence | 15 | 6.0 | 8.5 | 0.90 | 1.27 | Both analyses show theoretical coherence, but BSI's integration of computational social science and natural language processing theories is more comprehensive. |
| Originality | 10 | 5.0 | 9.0 | 0.50 | 0.90 | BSI's shift from sentence-level to population-level analysis and the introduction of the 'Caricature Gap' metric demonstrate higher originality. |
| Applicability | 10 | 4.0 | 8.5 | 0.40 | 0.85 | BSI's framework offers more direct applicability, particularly through the 'Caricature Gap' metric, for assessing the realism of AI-generated text. |
| Transparency | 5 | 3.0 | 8.0 | 0.15 | 0.40 | Both analyses are transparent, but BSI provides more detailed evaluation criteria and a clearer methodology. |
| Depth of Analysis | 15 | 6.0 | 8.5 | 0.90 | 1.27 | BSI's analysis dives deeper into the structural, emotional, and ideological dimensions of the generated text, offering a more nuanced understanding. |

#### Final Scores

| Analysis | Score (/10) |
|---|---:|
| Raw | 6.25 |
| BSI | 8.97 |

#### Summary

- Winner: **bsi**
- Score difference: **+2.72**
- Criteria evaluated: **7**

#### Score Formula

Final score = Σ(weight × criterion score / 100)
