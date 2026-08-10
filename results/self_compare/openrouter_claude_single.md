# Comparison: machine learning medical diagnosis

## Run metadata
- bsi-benchmark version: 0.1.0
- git commit: 4d7bbfa2f1fa2aea31a0d61d16f2b97689eb6c95 (uncommitted local changes present)
- run timestamp (UTC): 2026-08-05T05:28:17Z
- methodology note: Scores are produced by BSIEvaluator, an offline lexical/keyword-based proxy for the seven BIO v1.0 dimensions (regex and keyword matching, not semantic understanding). They are first-pass triage signals, not a validated measurement of analytical quality, until checked against independent human judgement on a representative sample. Do not cite numeric BSI scores as a certified metric without that validation step.

> BSI prompt source (read it yourself, unedited): https://github.com/ibstrade11-source/behmanesh-index-prompt/blob/main/MASTER_PROMPT_BSI_v3.4.2.md

## Adoption of machine learning for medical diagnosis
*source: https://doi.org/10.14293/s2199-1006.1.sor-.pphmka6.v1 | doi: 10.14293/s2199-1006.1.sor-.pphmka6.v1*

| generator | mode | D1 | D2 | D3 | D4 | D5 | D6 | D7 | BSI | grounding_ratio | tag_coverage |
|---|---|---|---|---|---|---|---|---|---|---|---|
| openrouter | raw | 1.000 | 1.000 | 0.000 | 0.758 | 0.000 | 0.250 | 1.000 | 0.599 | 1.000 | 0.000 |
| openrouter | bsi | 0.178 | 1.000 | 0.000 | 0.979 | 0.000 | 0.500 | 0.500 | 0.451 | 1.000 | 0.000 |
