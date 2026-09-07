# Comparison: A Long History: From Universal Language to Artificial Intelligence

## Run metadata
- bsi-benchmark version: 0.1.0
- git commit: 89a941006de1ccab30f7a16e09f86841cd5991eb
- run timestamp (UTC): 2026-09-07T23:18:15Z
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
| Criteria source | heuristic_fallback |
| Score scale | 0-10 |
| Weight sum | 100 |

#### Judge Reasoning

**Winner:** bsi

No LLM judge was available or its response could not be parsed -- this result is from a fixed keyword-presence heuristic, not an independent LLM judgement. Treat it as a placeholder, not a real evaluation.

#### Criteria Selected by Judge

| Criterion | Weight | Raw (/10) | BSI (/10) | Weighted Raw | Weighted BSI | Explanation |
|---|---:|---:|---:|---:|---:|---|
| structural_layers | 30 | 0.0 | 10.0 | 0.00 | 3.00 | Presence of analytical layers |
| epistemic_separation | 20 | 0.0 | 0.0 | 0.00 | 0.00 | Fact / inference / speculation separation |
| uncertainty_awareness | 20 | 10.0 | 2.0 | 2.00 | 0.40 | Recognition of uncertainty |
| evidence_grounding | 15 | 6.0 | 8.0 | 0.90 | 1.20 | Grounding in evidence |
| analysis_depth | 15 | 10.0 | 10.0 | 1.50 | 1.50 | Analytical coverage |

#### Final Scores

| Analysis | Score (/10) |
|---|---:|
| Raw | 4.40 |
| BSI | 6.10 |

#### Summary

- Winner: **bsi**
- Score difference: **+1.70**
- Criteria evaluated: **5**

#### Score Formula

Final score = Σ(weight × criterion score / 100)
