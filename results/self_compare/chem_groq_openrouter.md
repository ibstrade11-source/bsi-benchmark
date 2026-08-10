# Comparison: chemistry

## Run metadata
- bsi-benchmark version: 0.1.0
- git commit: 302bfb085d5c4201756ec36e02199b9f5c65c9db
- run timestamp (UTC): 2026-08-09T19:29:30Z
- methodology: Scores/judgements come from an independent LLM judge (see comparison/judge.py) instructed not to reuse BSI's own D1-D7/EIG vocabulary and to choose its own evaluation criteria. If no judge model is available or its response cannot be parsed, the run falls back to a simple keyword-presence heuristic -- the stored record's own 'criteria_source' field ('llm' vs 'heuristic_fallback') always says honestly which one produced a given result. Neither path is a validated measurement of analytical quality until checked against independent human judgement on a representative sample.

## Guest Editorial: Special Topic on Data-enabled Theoretical Chemistry

*source:* http://arxiv.org/abs/1806.02690v2
*doi:* 10.1063/1.5043213

### Judge Evaluation

#### Judge Information

| Field | Value |
|---|---|
| Criteria source | llm |
| Score scale | 0-10 |
| Weight sum | 100.0 |

#### Judge Reasoning

**Winner:** raw

RAW correctly identifies the article as a guest editorial, accurately describes its three actual functions (survey, glossary, accessibility framing), and avoids category errors. BSI fundamentally misclassifies the editorial as a research paper, applies an entire research-evaluation apparatus (7 criteria, CreativeValueAdd, layer analysis, EIG, REIG) to it, and generates detailed but hallucinated 'findings' about methodology, results, innovation, and causal mechanisms that do not exist in the editorial. BSI's framework is not merely unhelpful but actively detrimental for this article type, yielding negative incremental value.

#### Criteria Selected by Judge

| Criterion | Weight | Raw (/10) | BSI (/10) | Weighted Raw | Weighted BSI | Explanation |
|---|---:|---:|---:|---:|---:|---|
| Genre Recognition & Type-Appropriate Analysis | 25 | 10.0 | 2.0 | 2.50 | 0.50 | This is the most critical criterion because the article is explicitly a Guest Editorial introducing a special topic, not a research paper. RAW correctly identifies it as an 'introductory piece that sets the stage' and 'not presenting original research.' BSI fundamentally misclassifies it, evaluating it as if it were a research article with methodology, results, discussion, and innovation claims. |
| Accuracy of Content Description | 20 | 9.0 | 3.0 | 1.80 | 0.60 | RAW accurately describes the threefold contribution: survey of contributions, glossary of ML terms, and facilitating reader accessibility. BSI mentions the glossary but incorrectly attributes research claims ('core claim: data can be used as a powerful tool') to the editorial itself rather than recognizing it as an overview of other papers. |
| Understanding of Editorial Purpose | 20 | 9.0 | 2.0 | 1.80 | 0.40 | Editorials serve to frame, contextualize, and provide accessibility for a collection. RAW captures this: 'inform, educate, and provide context for the subsequent articles.' BSI entirely misses this purpose, instead searching for research contributions, mechanisms, and generative capacity within the editorial itself. |
| Avoidance of Category Errors | 15 | 10.0 | 1.0 | 1.50 | 0.15 | BSI commits severe category errors by applying a full research-paper evaluation rubric (innovation, methodology, results, discussion, conclusion, EIG analysis, REIG compliance) to an editorial. RAW avoids this entirely, noting the article is 'rather than presenting original research or groundbreaking findings.' |
| Identification of Actual Contributions | 10 | 9.0 | 3.0 | 0.90 | 0.30 | RAW specifically identifies the survey function, the glossary resource, and the accessibility goal. BSI notes the glossary but conflates the editorial with the special topic's research papers, attributing their content ('predicting chemical properties, designing new materials') to the editorial itself. |
| Analytical Coherence & Relevance | 10 | 9.0 | 4.0 | 0.90 | 0.40 | RAW's analysis is coherent, concise, and directly relevant to the actual article. BSI's analysis is internally consistent within its own framework but irrelevant to the actual editorial, producing elaborate but misdirected output (CreativeValueAdd, layer analysis, EIG, REIG) that addresses a phantom research paper. |

#### Final Scores

| Analysis | Score (/10) |
|---|---:|
| Raw | 9.40 |
| BSI | 2.35 |

#### Summary

- Winner: **raw**
- Score difference: **-7.05**
- Criteria evaluated: **6**

#### Score Formula

Final score = Σ(weight × criterion score / 100)
