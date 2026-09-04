# Comparison: cognitive psychology decision making

## Run metadata
- bsi-benchmark version: 0.1.0
- git commit: 7aa5a8270a580f6f5da60c2873fce47f5396eaec
- run timestamp (UTC): 2026-09-04T20:11:23Z
- methodology: Scores/judgements come from an independent LLM judge (see comparison/judge.py) instructed not to reuse BSI's own D1-D7/EIG vocabulary and to choose its own evaluation criteria. If no judge model is available or its response cannot be parsed, the run falls back to a simple keyword-presence heuristic -- the stored record's own 'criteria_source' field ('llm' vs 'heuristic_fallback') always says honestly which one produced a given result. Neither path is a validated measurement of analytical quality until checked against independent human judgement on a representative sample.

> BSI prompt source: https://github.com/ibstrade11-source/behmanesh-index-prompt/blob/main/MASTER_PROMPT_BSI_v3.4.2.md

## The Cognitive Revolution and the Political Psychology of Elite Decision Making

*source:* https://openalex.org/W3121340552
*doi:* https://doi.org/10.1017/s1537592713001084

### Judge Evaluation

#### Judge Information

| Field | Value |
|---|---|
| Criteria source | llm |
| Score scale | 0-10 |
| Weight sum | 100.0 |

#### Judge Reasoning

**Winner:** bsi

BSI offers a richer, more rigorous, and innovative evaluation of the article, while RAW remains a shallow summary. The BSI assessment improves upon RAW in every substantive criterion, justifying a clear BSI win.

#### Criteria Selected by Judge

| Criterion | Weight | Raw (/10) | BSI (/10) | Weighted Raw | Weighted BSI | Explanation |
|---|---:|---:|---:|---:|---:|---|
| Comprehensiveness of Argumentation | 20 | 5.0 | 9.0 | 1.00 | 1.80 | Raw analysis summarizes only the abstract and lists claims without elaborating on how they connect; BSI provides detailed narrative, context, and logical flow. |
| Depth of Theoretical Insight | 20 | 6.0 | 9.0 | 1.20 | 1.80 | Raw mentions dual-process trade-off and overconfidence, but does not explore underlying mechanisms; BSI explicitly discusses the paradox and its implications. |
| Integration of Empirical Evidence | 20 | 7.0 | 8.0 | 1.40 | 1.60 | Raw notes the US‑North Korea case but offers no evidence assessment; BSI evaluates the case study’s methodological strengths and weaknesses. |
| Methodological Rigor and Critique | 15 | 5.0 | 8.0 | 0.75 | 1.20 | Raw lacks any methodological critique; BSI discusses sampling, selection bias, and causal inference. |
| Innovation and Creative Value | 15 | 7.0 | 9.0 | 1.05 | 1.35 | Raw does not highlight novelty beyond summarization; BSI identifies a novel elite‑cognition paradox and its broader relevance. |
| Clarity and Readability | 10 | 8.0 | 7.0 | 0.80 | 0.70 | Raw is succinct and easy to read; BSI is longer but more complex, slightly reducing immediate accessibility. |

#### Final Scores

| Analysis | Score (/10) |
|---|---:|
| Raw | 6.20 |
| BSI | 8.45 |

#### Summary

- Winner: **bsi**
- Score difference: **+2.25**
- Criteria evaluated: **6**

#### Score Formula

Final score = Σ(weight × criterion score / 100)
