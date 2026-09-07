# Comparison: A Long History: From Universal Language to Artificial Intelligence

## Run metadata
- bsi-benchmark version: 0.1.0
- git commit: 89a941006de1ccab30f7a16e09f86841cd5991eb
- run timestamp (UTC): 2026-09-07T23:06:25Z
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

Across weighted criteria, the BSI analysis scores 8.75/10 while RAW scores 7.83/10. BSI offers a sharper theoretical lens and stronger practical framing, thus surpassing RAW in overall evaluative merit.

#### Criteria Selected by Judge

| Criterion | Weight | Raw (/10) | BSI (/10) | Weighted Raw | Weighted BSI | Explanation |
|---|---:|---:|---:|---:|---:|---|
| Logical Coherence | 25 | 8.0 | 9.0 | 2.00 | 2.25 | Both analyses present a clear chronological narrative, but the BSI version explicitly links the stages and shows tighter argumentative flow. |
| Evidential Support | 15 | 6.0 | 5.0 | 0.90 | 0.75 | RAW cites specific historical sources; BSI acknowledges limited access to full text, reducing confidence in evidence depth. |
| Theoretical Depth | 20 | 7.0 | 9.0 | 1.40 | 1.80 | BSI incorporates advanced STS concepts (co‑constitution, epistemic assumptions) more explicitly than RAW. |
| Methodological Rigor | 10 | 6.0 | 6.0 | 0.60 | 0.60 | Both analyses acknowledge the genealogical method but lack detailed procedural description. |
| Practical Relevance | 15 | 7.0 | 8.0 | 1.05 | 1.20 | BSI highlights policy implications more directly, referencing governance and equity. |
| Communication Quality | 15 | 8.0 | 9.0 | 1.20 | 1.35 | BSI uses precise terminology and concise structure; RAW is slightly more verbose. |

#### Final Scores

| Analysis | Score (/10) |
|---|---:|
| Raw | 7.15 |
| BSI | 7.95 |

#### Summary

- Winner: **bsi**
- Score difference: **+0.80**
- Criteria evaluated: **6**

#### Score Formula

Final score = Σ(weight × criterion score / 100)
