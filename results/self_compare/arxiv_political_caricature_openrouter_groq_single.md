# Comparison: The Algorithmic Caricature: Auditing LLM-Generated Political Discourse Across Crisis Events

## Run metadata
- bsi-benchmark version: 0.1.0
- git commit: 302bfb085d5c4201756ec36e02199b9f5c65c9db
- run timestamp (UTC): 2026-08-10T04:05:58Z
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

BSI's analysis provides a more comprehensive and innovative evaluation of the Caricature Gap, and its use of a paired design and control of context variables provides stronger evidence for its claims. The introduction of the Caricature Gap metric and its application to population-level auditing is a significant contribution to the field.

#### Criteria Selected by Judge

| Criterion | Weight | Raw (/10) | BSI (/10) | Weighted Raw | Weighted BSI | Explanation |
|---|---:|---:|---:|---:|---:|---|
| Epistemic Validity | 20 | 8.0 | 9.0 | 1.60 | 1.80 | Both analyses demonstrate high epistemic validity, but BSI's use of a paired design and control of context variables provides stronger evidence. |
| Methodological Rigor | 18 | 7.0 | 9.0 | 1.26 | 1.62 | BSI's methodological rigor is higher due to its use of a more comprehensive dataset and a clearer explanation of the calculation of the Caricature Gap metric. |
| Novelty of Contribution | 15 | 6.0 | 8.0 | 0.90 | 1.20 | Both analyses provide novel contributions, but BSI's introduction of the Caricature Gap metric and its application to population-level auditing is more innovative. |
| Data Quality and Quantity | 12 | 8.0 | 9.0 | 0.96 | 1.08 | BSI's use of a larger and more diverse dataset provides stronger evidence for its claims. |
| Theoretical Soundness | 10 | 7.0 | 8.0 | 0.70 | 0.80 | Both analyses demonstrate strong theoretical soundness, but BSI's use of a more comprehensive framework provides a clearer understanding of the underlying mechanisms. |
| Practical Implications | 8 | 6.0 | 7.0 | 0.48 | 0.56 | BSI's analysis provides more practical implications for the development of more effective detection methods and the improvement of LLMs. |
| Clarity and Presentation | 5 | 8.0 | 8.0 | 0.40 | 0.40 | Both analyses are well-presented, but BSI's use of clear and concise language provides a slightly better reading experience. |
| Relevance to the Field | 12 | 7.0 | 8.0 | 0.84 | 0.96 | BSI's analysis is more relevant to the field due to its focus on the critical issue of detecting synthetic political discourse. |

#### Final Scores

| Analysis | Score (/10) |
|---|---:|
| Raw | 7.14 |
| BSI | 8.42 |

#### Summary

- Winner: **bsi**
- Score difference: **+1.28**
- Criteria evaluated: **8**

#### Score Formula

Final score = Σ(weight × criterion score / 100)
