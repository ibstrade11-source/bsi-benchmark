# Comparison: A Long History: From Universal Language to Artificial Intelligence

## Run metadata
- bsi-benchmark version: 0.1.0
- git commit: 89a941006de1ccab30f7a16e09f86841cd5991eb
- run timestamp (UTC): 2026-09-07T22:29:09Z
- methodology: Scores/judgements come from an independent LLM judge (see comparison/judge.py) instructed not to reuse BSI's own D1-D7/EIG vocabulary and to choose its own evaluation criteria. If no judge model is available or its response cannot be parsed, the run falls back to a simple keyword-presence heuristic -- the stored record's own 'criteria_source' field ('llm' vs 'heuristic_fallback') always says honestly which one produced a given result. Neither path is a validated measurement of analytical quality until checked against independent human judgement on a representative sample.

> BSI prompt source: https://github.com/ibstrade11-source/behmanesh-index-prompt/blob/main/MASTER_PROMPT_BSI_v3.4.2.md

## Benchmark status

- status: **benchmarkable**

## Retrieval validation

- retrieval status: **accepted**
- query type: title
- selected title: A Long History: From Universal Language to Artificial Intelligence
- selected candidate rank: 1
- title match score: 1.0
- acceptance threshold: 0.72
- rejected candidates: 0

## A Long History: From Universal Language to Artificial Intelligence

*source:* https://openalex.org/W7160269223
*doi:* https://doi.org/10.1353/tech.2026.a988849

### Judge Evaluation

#### Judge Information

| Field | Value |
|---|---|
| Criteria source | llm |
| Score scale | 0-10 |
| Weight sum | 100.0 |

#### Judge Reasoning

**Winner:** bsi

BSI provides a deeper, more structured, and conceptually innovative analysis that advances beyond the RAW assessment.

#### Criteria Selected by Judge

| Criterion | Weight | Raw (/10) | BSI (/10) | Weighted Raw | Weighted BSI | Explanation |
|---|---:|---:|---:|---:|---:|---|
| Historical Contextualization | 30 | 7.0 | 9.0 | 2.10 | 2.70 | RAW notes historical continuity but lacks depth; BSI explicitly traces multi‑century genealogy and contextualizes AI within that lineage. |
| Argument Coherence | 25 | 8.0 | 9.0 | 2.00 | 2.25 | Both analyses present clear arguments; BSI scores slightly higher due to more explicit causal linkage across layers. |
| Evidence Integration | 20 | 6.0 | 8.0 | 1.20 | 1.60 | RAW relies on abstract references; BSI lists specific historical milestones and sources, giving stronger evidentiary support. |
| Conceptual Innovation | 15 | 6.0 | 8.0 | 0.90 | 1.20 | BSI reframes AI as a genealogical continuation rather than a rupture, a novel conceptual stance not present in RAW. |
| Practical Implications | 10 | 5.0 | 7.0 | 0.50 | 0.70 | BSI offers policy insights and strategic viewpoints; RAW is more descriptive. |

#### Final Scores

| Analysis | Score (/10) |
|---|---:|
| Raw | 6.70 |
| BSI | 8.45 |

#### Summary

- Winner: **bsi**
- Score difference: **+1.75**
- Criteria evaluated: **5**

#### Score Formula

Final score = Σ(weight × criterion score / 100)
