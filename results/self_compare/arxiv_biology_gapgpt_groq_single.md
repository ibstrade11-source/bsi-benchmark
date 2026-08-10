# Comparison: biology molecular biology genetics cell biology

## Run metadata
- bsi-benchmark version: 0.1.0
- git commit: 302bfb085d5c4201756ec36e02199b9f5c65c9db
- run timestamp (UTC): 2026-08-10T06:38:59Z
- methodology: Scores/judgements come from an independent LLM judge (see comparison/judge.py) instructed not to reuse BSI's own D1-D7/EIG vocabulary and to choose its own evaluation criteria. If no judge model is available or its response cannot be parsed, the run falls back to a simple keyword-presence heuristic -- the stored record's own 'criteria_source' field ('llm' vs 'heuristic_fallback') always says honestly which one produced a given result. Neither path is a validated measurement of analytical quality until checked against independent human judgement on a representative sample.

> BSI prompt source: https://github.com/ibstrade11-source/behmanesh-index-prompt/blob/main/MASTER_PROMPT_BSI_v3.4.2.md

## Bayesian uncertainty analysis for complex systems biology models: emulation, global parameter searches and evaluation of gene functions

*source:* http://arxiv.org/abs/1607.06358v2
*doi:* 10.1186/s12918-017-0484-3

### Judge Evaluation

#### Judge Information

| Field | Value |
|---|---|
| Criteria source | llm |
| Score scale | 0-10 |
| Weight sum | 100.0 |

#### Judge Reasoning

**Winner:** bsi

BSI analysis demonstrates a higher overall quality, with stronger scores in relevance to systems biology challenges, methodological soundness, and practical applicability

#### Criteria Selected by Judge

| Criterion | Weight | Raw (/10) | BSI (/10) | Weighted Raw | Weighted BSI | Explanation |
|---|---:|---:|---:|---:|---:|---|
| Relevance to Systems Biology Challenges | 25 | 8.0 | 9.0 | 2.00 | 2.25 | BSI analysis demonstrates a higher relevance to systems biology challenges |
| Methodological Soundness | 20 | 7.0 | 8.0 | 1.40 | 1.60 | BSI analysis provides a more comprehensive and well-justified methodology |
| Innovativeness and Originality | 15 | 6.0 | 8.0 | 0.90 | 1.20 | BSI analysis introduces new and innovative approaches to addressing systems biology challenges |
| Practical Applicability | 15 | 8.0 | 9.0 | 1.20 | 1.35 | BSI analysis demonstrates a higher practical applicability |
| Statistical Validity | 10 | 6.0 | 8.0 | 0.60 | 0.80 | BSI analysis provides a more statistically valid approach |
| Biological Interpretability | 10 | 7.0 | 8.0 | 0.70 | 0.80 | BSI analysis provides more biologically meaningful insights and interpretations |
| Clarity and Coherence | 5 | 8.0 | 7.0 | 0.40 | 0.35 | RAW analysis is clearer and more well-organized, but BSI analysis is still coherent and easy to follow |

#### Final Scores

| Analysis | Score (/10) |
|---|---:|
| Raw | 7.20 |
| BSI | 8.35 |

#### Summary

- Winner: **bsi**
- Score difference: **+1.15**
- Criteria evaluated: **7**

#### Score Formula

Final score = Σ(weight × criterion score / 100)
