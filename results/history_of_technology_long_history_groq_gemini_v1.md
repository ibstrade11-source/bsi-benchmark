# Comparison: A Long History: From Universal Language to Artificial Intelligence

## Run metadata
- bsi-benchmark version: 0.1.0
- git commit: 89a941006de1ccab30f7a16e09f86841cd5991eb
- run timestamp (UTC): 2026-09-07T22:43:48Z
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

**Winner:** raw

RAW delivers a more cohesive, scientifically grounded, and transparent synthesis of the paper's thesis and STS contributions without template artifacts or numerical discrepancies. While BSI offers structured layer decomposition and gap analysis, its execution is weighed down by internal scoring mismatches and formulaic compliance checks.

#### Criteria Selected by Judge

| Criterion | Weight | Raw (/10) | BSI (/10) | Weighted Raw | Weighted BSI | Explanation |
|---|---:|---:|---:|---:|---:|---|
| Core Conceptual Reconstruction & Historical Lineage | 25 | 9.0 | 8.5 | 2.25 | 2.12 | RAW provides a clean, highly accurate 5-point breakdown of the historical continuum from 17th-century universal language projects to contemporary AI. BSI also captures this effectively in its executive summary and latent layering, though with slightly more meta-textual overhead. |
| Epistemic & Sociotechnical Depth | 25 | 8.5 | 8.5 | 2.12 | 2.12 | Both analyses excel at identifying the co-constitution of epistemology and technology. RAW clearly highlights the STS framing, while BSI adds value through its latent layer breakdown of epistemic activation, encoding, and computability feedback loops. |
| Methodological and Evaluative Rigor | 20 | 8.0 | 7.0 | 1.60 | 1.40 | RAW objectively outlines the article's contributions across fields without unsupported claims. BSI applies a multi-dimensional rubric (7-criteria and REIG audit), but displays minor arithmetic inconsistencies (54/70 equates to 7.7/10, yet is reported as 8.2/10) and uses template-heavy compliance assertions. |
| Actionability & Research Implications | 15 | 8.0 | 8.0 | 1.20 | 1.20 | RAW articulates clear implications for AI governance and historical-empirical research. BSI provides structured Epistemic Information Gap (EIG) identification, specifically pointing toward multicultural NLP integration and hybrid algorithmic models. |
| Clarity, Coherence, and Structural Consistency | 15 | 9.0 | 7.5 | 1.35 | 1.12 | RAW is concise, fluent, and highly readable. BSI is systematically organized into matrices, but suffers from slight formulaic rigidity, language mismatch relative to the source title, and calculation discrepancies. |

#### Final Scores

| Analysis | Score (/10) |
|---|---:|
| Raw | 8.52 |
| BSI | 7.96 |

#### Summary

- Winner: **raw**
- Score difference: **-0.56**
- Criteria evaluated: **5**

#### Score Formula

Final score = Σ(weight × criterion score / 100)
