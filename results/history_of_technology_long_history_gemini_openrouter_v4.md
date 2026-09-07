# Comparison: A Long History: From Universal Language to Artificial Intelligence

## Run metadata
- bsi-benchmark version: 0.1.0
- git commit: 89a941006de1ccab30f7a16e09f86841cd5991eb
- run timestamp (UTC): 2026-09-07T22:23:59Z
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

BSI delivers substantially deeper, more structured, and more critical engagement with the article's historical-genealogical thesis across all seven weighted criteria. RAW provides only a surface-level summary of claims without analytical depth, gap analysis, mechanism identification, or critical evaluation. BSI's incremental value is high because it transforms a descriptive summary into a multi-layered epistemic assessment that exposes both the article's structural coherence and its specific analytical vulnerabilities (e.g., emergent abilities, causal attribution gaps).

#### Criteria Selected by Judge

| Criterion | Weight | Raw (/10) | BSI (/10) | Weighted Raw | Weighted BSI | Explanation |
|---|---:|---:|---:|---:|---:|---|
| Historical Genealogical Depth | 25 | 3.0 | 9.0 | 0.75 | 2.25 | Article's core project is tracing AI language models to 17th-century universal language schemes; RAW only mentions this in passing while BSI provides detailed multi-century tracing with specific intellectual lineages. |
| Theoretical/Conceptual Rigor | 20 | 4.0 | 9.0 | 0.80 | 1.80 | Co-constitution of language and computation is the central thesis; RAW states it without analysis while BSI unpacks ontological reductionism, feedback loops, and leverage points with conceptual precision. |
| Critical Intervention Value | 15 | 5.0 | 9.0 | 0.75 | 1.35 | Challenging the 'radical rupture' narrative is the article's main intervention; RAW merely reports the claim while BSI evaluates its resilience against emergence arguments and identifies where the genealogy needs strengthening. |
| Interdisciplinary Synthesis | 15 | 3.0 | 9.0 | 0.45 | 1.35 | Article bridges STS, history of philosophy, linguistics, information theory, and AI; RAW lists fields but BSI demonstrates successful synthesis across Shannon, Leibniz, transformer architectures, and pragmatic language models. |
| Mechanism/Process Analysis | 10 | 2.0 | 8.0 | 0.20 | 0.80 | Understanding HOW historical continuity operates (not just THAT it exists); RAW provides none while BSI identifies ontological reductionism as mechanism, reinforcing feedback loops, and definitional leverage points. |
| Epistemic Gap Identification | 10 | 2.0 | 8.0 | 0.20 | 0.80 | Article's value lies partly in exposing what current AI discourse misses; RAW identifies no gaps while BSI's EIG analysis articulates both an epistemic-ontological gap and a causal attribution gap regarding emergent abilities. |
| Practical/Policy Relevance | 5 | 3.0 | 8.0 | 0.15 | 0.40 | Article claims historical understanding prevents AI governance hype; RAW mentions this superficially while BSI evaluates policy value concretely and links to governance implications. |

#### Final Scores

| Analysis | Score (/10) |
|---|---:|
| Raw | 3.30 |
| BSI | 8.75 |

#### Summary

- Winner: **bsi**
- Score difference: **+5.45**
- Criteria evaluated: **7**

#### Score Formula

Final score = Σ(weight × criterion score / 100)
