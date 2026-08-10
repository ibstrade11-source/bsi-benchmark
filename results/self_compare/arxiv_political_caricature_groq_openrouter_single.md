# Comparison: The Algorithmic Caricature: Auditing LLM-Generated Political Discourse Across Crisis Events

## Run metadata
- bsi-benchmark version: 0.1.0
- git commit: 302bfb085d5c4201756ec36e02199b9f5c65c9db
- run timestamp (UTC): 2026-08-10T04:49:49Z
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

**Winner:** raw

RAW accurately summarizes the article's technical core (four dimensions, Caricature Gap, event-dependent findings) and its theoretical positioning (population-level auditing vs. text detection) in clear, coherent language. BSI introduces multiple framework artifacts (7-criterion table, CreativeValueAdd, Manifest/Latent/Meta layers, EIG, REIG) but populates them with generic or template content that does not engage the article's specifics. BSI's scores are unexplained, its limitation assessment is vague, and its mixed-language presentation impedes clarity. No BSI capability is realized effectively here; the analysis adds confusion without analytical benefit.

#### Criteria Selected by Judge

| Criterion | Weight | Raw (/10) | BSI (/10) | Weighted Raw | Weighted BSI | Explanation |
|---|---:|---:|---:|---:|---:|---|
| Accuracy of technical summary | 25 | 9.0 | 7.0 | 2.25 | 1.75 | The article introduces a specific four-dimensional framework (emotional intensity, structural regularity, lexical-ideological framing, cross-event dependency), a novel measure (Caricature Gap), and event-dependent findings. Accurate capture of these technical details is essential for any meaningful evaluation. |
| Understanding of theoretical contribution | 20 | 8.0 | 6.0 | 1.60 | 1.20 | The core contribution is the population-level auditing framework as a complement to text-detection methods. An analysis must distinguish this from mere text-quality assessment to reflect the article's actual advance. |
| Critical evaluation of findings | 20 | 7.0 | 5.0 | 1.40 | 1.00 | The finding that gaps are larger in fast-moving, decentralized crises and smaller in formal/institutional events is a key empirical result. Proper representation of this nuance indicates analytical depth. |
| Assessment of limitations | 15 | 6.0 | 5.0 | 0.90 | 0.75 | The article acknowledges database and evaluation limitations. A scientific evaluation should surface these rather than presenting the study as definitive. |
| Clarity and coherence | 10 | 9.0 | 4.0 | 0.90 | 0.40 | Mixed-language presentation, disconnected framework tables (CreativeValueAdd, EIG, REIG), and template-like compliance checks reduce the BSI analysis's communicative effectiveness. |
| Depth of analytical insight | 10 | 6.0 | 5.0 | 0.60 | 0.50 | Going beyond summary to interpret implications for LLM development, crisis communication, or computational social science adds value. RAW offers modest insight; BSI's layer/EIG structure appears performative rather than substantive for this article. |

#### Final Scores

| Analysis | Score (/10) |
|---|---:|
| Raw | 7.65 |
| BSI | 5.60 |

#### Summary

- Winner: **raw**
- Score difference: **-2.05**
- Criteria evaluated: **6**

#### Score Formula

Final score = Σ(weight × criterion score / 100)
