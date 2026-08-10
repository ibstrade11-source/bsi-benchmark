# Comparison: political caricature LLM-generated political discourse crisis events

## Run metadata
- bsi-benchmark version: 0.1.0
- git commit: 302bfb085d5c4201756ec36e02199b9f5c65c9db
- run timestamp (UTC): 2026-08-10T05:09:44Z
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

BSI outperforms RAW on the three highest-weighted criteria that distinguish a scientific evaluation from a summary: critical assessment of limitations (+4), theoretical synthesis (+3), and field contextualization (+3). RAW is accurate and clear but functions as an extended abstract; BSI functions as a peer review. The capability assessment confirms BSI's framework added high incremental value for this article without inflating scores artificially.

#### Criteria Selected by Judge

| Criterion | Weight | Raw (/10) | BSI (/10) | Weighted Raw | Weighted BSI | Explanation |
|---|---:|---:|---:|---:|---:|---|
| Accuracy of Technical Summary | 25 | 9.0 | 9.0 | 2.25 | 2.25 | The article's core is its large-scale empirical methodology (1.7M posts, 9 crises, 4 dimensions, Caricature Gap metric). Both analyses must accurately capture these technical specifics to be useful. |
| Coverage of Key Contributions | 20 | 8.0 | 9.0 | 1.60 | 1.80 | The article explicitly frames three contribution types (conceptual, methodological, empirical). An evaluation must reflect all three to represent the article's self-presentation. |
| Critical Assessment of Limitations | 15 | 4.0 | 8.0 | 0.60 | 1.20 | Scientific evaluation requires identifying scope boundaries (US/English-only, commercial models only, crisis-type generalization). The article itself discusses these; a strong analysis must surface them. |
| Synthesis of Theoretical Implications | 15 | 6.0 | 9.0 | 0.90 | 1.35 | The article claims a paradigm shift from Turing Test to Collective Turing Test. An analysis that unpacks the latent mechanisms (RLHF convergence, feedback loops) and meta-level significance adds distinct scientific value. |
| Identification of Novel Metrics/Frameworks | 10 | 8.0 | 9.0 | 0.80 | 0.90 | The Caricature Gap and Social Realism are the article's flagship constructs. Explicit naming and explanation of these is necessary for any analysis to serve as a usable reference. |
| Contextualization Within Broader Field | 10 | 5.0 | 8.0 | 0.50 | 0.80 | The work sits at the intersection of CSS, NLP, and AI safety. Placing it relative to perplexity-based detection, alignment research, and disinformation studies helps readers gauge its field-level impact. |
| Clarity and Organization | 5 | 9.0 | 7.0 | 0.45 | 0.35 | While secondary to analytical depth, clear structure enables efficient uptake. RAW's concise sections score highly; BSI's density and Persian language slightly reduce accessibility for an English-speaking scientific audience. |

#### Final Scores

| Analysis | Score (/10) |
|---|---:|
| Raw | 7.10 |
| BSI | 8.65 |

#### Summary

- Winner: **bsi**
- Score difference: **+1.55**
- Criteria evaluated: **7**

#### Score Formula

Final score = Σ(weight × criterion score / 100)
