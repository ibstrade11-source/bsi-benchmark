# Comparison: cognitive psychology

## Run metadata
- bsi-benchmark version: 0.1.0
- git commit: ae9d88e053f2ead621a781a585eb562ccf72fd1f
- run timestamp (UTC): 2026-09-04T23:03:40Z
- methodology: Scores/judgements come from an independent LLM judge (see comparison/judge.py) instructed not to reuse BSI's own D1-D7/EIG vocabulary and to choose its own evaluation criteria. If no judge model is available or its response cannot be parsed, the run falls back to a simple keyword-presence heuristic -- the stored record's own 'criteria_source' field ('llm' vs 'heuristic_fallback') always says honestly which one produced a given result. Neither path is a validated measurement of analytical quality until checked against independent human judgement on a representative sample.

> BSI prompt source: https://github.com/ibstrade11-source/behmanesh-index-prompt/blob/main/MASTER_PROMPT_BSI_v3.4.2.md

## Kurt Lewin, psychological constructs and sources of brain cognitive activity

*source:* http://arxiv.org/abs/1711.01767v1

### Judge Evaluation

#### Judge Information

| Field | Value |
|---|---|
| Criteria source | llm |
| Score scale | 0-10 |
| Weight sum | 100.0 |

#### Judge Reasoning

**Winner:** bsi

The BSI analysis scores higher across all criteria, achieving a superior overall score and providing added depth and actionable pathways that the RAW analysis lacks. Hence BSI is the winner.

#### Criteria Selected by Judge

| Criterion | Weight | Raw (/10) | BSI (/10) | Weighted Raw | Weighted BSI | Explanation |
|---|---:|---:|---:|---:|---:|---|
| Logical Coherence | 20 | 7.0 | 8.2 | 1.40 | 1.64 | Both analyses present a clear narrative, but the BSI analysis explicitly ties Lewinian constructs to modern attractor‑network theory, offering a tighter logical flow. |
| Explanatory Power | 20 | 7.0 | 8.3 | 1.40 | 1.66 | The BSI analysis maps Lewin’s life space and valence onto neural state‑space dynamics, yielding a more comprehensive explanation of cognition and psychopathology. |
| Empirical Grounding | 15 | 6.5 | 7.8 | 0.97 | 1.17 | RAW relies primarily on theoretical synthesis; BSI, while still theoretical, references current neuroimaging, BCI, and RDoC initiatives, providing stronger empirical context. |
| Methodological Rigor | 15 | 6.8 | 8.1 | 1.02 | 1.22 | BSI’s structured BSI framework introduces layers (manifest, latent, etc.), giving a clearer methodological scaffold than RAW’s descriptive approach. |
| Novelty | 20 | 7.5 | 8.4 | 1.50 | 1.68 | BSI uniquely integrates Lewin’s historical theory with contemporary computational neuroscience, a novelty beyond RAW’s historical review. |
| Practical Actionability | 10 | 7.0 | 8.0 | 0.70 | 0.80 | BSI outlines concrete paths (BCI validation, simulation, RDoC implementation) while RAW remains more conceptual. |

#### Final Scores

| Analysis | Score (/10) |
|---|---:|
| Raw | 6.99 |
| BSI | 8.17 |

#### Summary

- Winner: **bsi**
- Score difference: **+1.18**
- Criteria evaluated: **6**

#### Score Formula

Final score = Σ(weight × criterion score / 100)
