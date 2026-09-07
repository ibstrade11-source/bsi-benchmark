# Comparison: A Long History: From Universal Language to Artificial Intelligence

## Run metadata
- bsi-benchmark version: 0.1.0
- git commit: 89a941006de1ccab30f7a16e09f86841cd5991eb
- run timestamp (UTC): 2026-09-07T21:53:03Z
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

BSI wins on analytical depth, structural rigor, and critical generativity. It transforms the article's implicit genealogy into an explicit three-layer causal model, quantifies theoretical novelty, and produces actionable research gaps—all while passing a formal self-audit. RAW remains a useful executive summary but lacks the mechanistic and meta-critical dimensions that BSI supplies.

#### Criteria Selected by Judge

| Criterion | Weight | Raw (/10) | BSI (/10) | Weighted Raw | Weighted BSI | Explanation |
|---|---:|---:|---:|---:|---:|---|
| Historical Genealogy Coherence | 25 | 7.0 | 9.0 | 1.75 | 2.25 | RAW captures the continuity claim but stays at summary level; BSI's three-layer mapping (Manifest/Latent/Meta) explicitly traces the genealogy from 17th-century universal language through information theory to transformer architectures, showing mechanistic links. |
| STS/Framing Insight | 20 | 7.0 | 9.0 | 1.40 | 1.80 | RAW names the STS reframing; BSI deepens it by exposing the epistemic assumptions (quantitative ontology, formal reductionism) and the meta-level critique of 'informational modernity' that the article only implies. |
| Conceptual Depth | 20 | 5.0 | 9.0 | 1.00 | 1.80 | RAW offers no theoretical elaboration; BSI synthesizes philosophy of language, Shannon information theory, STS, and NLP engineering into a combinatorial framework with scored Theoretical Depth (9/10) and CreativeValueAdd synthesis (88/100). |
| Critical Gap Identification | 15 | 3.0 | 8.0 | 0.45 | 1.20 | RAW identifies zero gaps; BSI's EIG section pinpoints three substantive gaps: continuity/rupture non-linearity, Western-centric genealogy, and symbolic vs. connectionist mechanistic divergence. |
| Structural/Methodological Rigor | 10 | 6.0 | 9.0 | 0.60 | 0.90 | RAW uses a simple two-section structure; BSI deploys a seven-criterion rubric, weighted CreativeValueAdd matrix, three-layer deep analysis, and a formal REIG self-audit against causal, generalization, measurement, and framing compliance. |
| Accessibility & Clarity | 10 | 9.0 | 6.0 | 0.90 | 0.60 | RAW is concise, jargon-light, and immediately readable; BSI is dense, bilingual, and assumes familiarity with BSI-specific constructs (Manifest/Latent/Meta, EIG, REIG), reducing accessibility for non-specialist readers. |

#### Final Scores

| Analysis | Score (/10) |
|---|---:|
| Raw | 6.10 |
| BSI | 8.55 |

#### Summary

- Winner: **bsi**
- Score difference: **+2.45**
- Criteria evaluated: **6**

#### Score Formula

Final score = Σ(weight × criterion score / 100)
