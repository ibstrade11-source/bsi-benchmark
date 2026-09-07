# Comparison: A Long History: From Universal Language to Artificial Intelligence

## Run metadata
- bsi-benchmark version: 0.1.0
- git commit: 89a941006de1ccab30f7a16e09f86841cd5991eb
- run timestamp (UTC): 2026-09-07T22:39:42Z
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

**Winner:** tie

RAW delivers an exceptionally crisp, well-structured, and error-free synthesis of the article's STS contributions and historical periods. BSI adds substantial depth via its multi-layer latent breakdown (e.g., mechanisms of logicization of authority, reification of abstraction, and feedback loops across epochs), but its score is balanced out by severe rendering glitches and a truncated finish.

#### Criteria Selected by Judge

| Criterion | Weight | Raw (/10) | BSI (/10) | Weighted Raw | Weighted BSI | Explanation |
|---|---:|---:|---:|---:|---:|---|
| Extraction & Representation of Core Arguments | 20 | 9.0 | 8.0 | 1.80 | 1.60 | RAW provides a pristine, accurate synthesis of the paper's three historical epochs and core claims. BSI accurately captures the core thesis as well, but suffers from distracting multilingual encoding/script glitches throughout the Persian text. |
| Genealogical & Epistemological Depth | 25 | 8.0 | 9.0 | 2.00 | 2.25 | BSI unpacks the epistemological trajectory in significant detail, identifying recurring structural patterns across historical phases (e.g., separating information from meaning, logicizing authority, and reifying abstraction). |
| Latent Systemic & Mechanistic Modeling | 25 | 7.0 | 8.0 | 1.75 | 2.00 | BSI maps the sociotechnical dynamics onto actionable leverage points (Donella Meadows framework) and latent epistemic shifts. RAW identifies the co-productionist stance well but does not elaborate systemic feedback mechanisms. |
| STS Conceptual Grounding & Precision | 15 | 9.0 | 8.0 | 1.35 | 1.20 | RAW precisely frames the STS/co-productionist contributions and historical continuity. BSI applies rich STS concepts (Foucauldian genealogy, Jasanoff's co-production) but incorporates extraneous non-Persian character corruptions. |
| Structural Completeness & Execution Quality | 15 | 9.0 | 5.0 | 1.35 | 0.75 | RAW is fully complete, concise, and cleanly structured. BSI suffers from severe multilingual text corruption artifacts (random Korean, Cyrillic, Vietnamese characters embedded in sentences) and ends abruptly mid-word in Section 4.3 due to token truncation. |

#### Final Scores

| Analysis | Score (/10) |
|---|---:|
| Raw | 8.25 |
| BSI | 7.80 |

#### Summary

- Winner: **tie**
- Score difference: **-0.45**
- Criteria evaluated: **5**

#### Score Formula

Final score = Σ(weight × criterion score / 100)
