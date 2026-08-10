# Comparison: Adoption of machine learning for medical diagnosis

## Run metadata
- bsi-benchmark version: 0.1.0
- git commit: 85f2f01c3cd0011931edf819e040580130965f66 (uncommitted local changes present)
- run timestamp (UTC): 2026-08-03T17:42:52Z
- methodology note: Scores are produced by BSIEvaluator, an offline lexical/keyword-based proxy for the seven BIO v1.0 dimensions (regex and keyword matching, not semantic understanding). They are first-pass triage signals, not a validated measurement of analytical quality, until checked against independent human judgement on a representative sample. Do not cite numeric BSI scores as a certified metric without that validation step.

> BSI prompt source (read it yourself, unedited): https://github.com/ibstrade11-source/behmanesh-index-prompt/blob/main/MASTER_PROMPT_BSI_v3.4.2.md

## Adoption of machine learning for medical diagnosis
*source: https://doi.org/10.14293/s2199-1006.1.sor-.pphmka6.v1 | doi: 10.14293/s2199-1006.1.sor-.pphmka6.v1*

| generator | mode | D1 | D2 | D3 | D4 | D5 | D6 | D7 | BSI | grounding_ratio | tag_coverage |
|---|---|---|---|---|---|---|---|---|---|---|---|
| local | raw | 1.000 | 1.000 | 0.000 | 0.622 | 0.000 | 0.125 | 0.500 | 0.541 | 1.000 | 0.000 |
| local | bsi | 1.000 | 1.000 | 0.000 | 0.838 | 0.000 | 0.375 | 1.000 | 0.622 | 1.000 | 0.000 |
