# Comparison: transformer attention mechanism

## Run metadata
- bsi-benchmark version: 0.1.0
- git commit: 6ca74058de582d7baa7334af0a164f48fcef2b82 (uncommitted local changes present)
- run timestamp (UTC): 2026-08-05T03:29:37Z
- methodology note: Scores are produced by BSIEvaluator, an offline lexical/keyword-based proxy for the seven BIO v1.0 dimensions (regex and keyword matching, not semantic understanding). They are first-pass triage signals, not a validated measurement of analytical quality, until checked against independent human judgement on a representative sample. Do not cite numeric BSI scores as a certified metric without that validation step.

> BSI prompt source (read it yourself, unedited): https://github.com/ibstrade11-source/behmanesh-index-prompt/blob/main/MASTER_PROMPT_BSI_v3.4.2.md

## Transformer-based Personalized Attention Mechanism for Medical Images with Clinical Records
*source: http://arxiv.org/abs/2206.03003v2*

| generator | mode | D1 | D2 | D3 | D4 | D5 | D6 | D7 | BSI | grounding_ratio | tag_coverage |
|---|---|---|---|---|---|---|---|---|---|---|---|
| mock | raw | 1.000 | 1.000 | 0.000 | 0.000 | 0.820 | 0.125 | 1.000 | 0.558 | 1.000 | 0.000 |
| mock | bsi | 1.000 | 1.000 | 0.708 | 0.264 | 1.000 | 0.125 | 1.000 | 0.752 | 1.000 | 0.273 |
| openrouter | raw | 1.000 | 1.000 | 0.000 | 0.739 | 0.444 | 0.250 | 0.500 | 0.624 | 1.000 | 0.000 |
| openrouter | bsi | 0.235 | 1.000 | 1.000 | 0.957 | 0.000 | 0.625 | 1.000 | 0.674 | 1.000 | 0.000 |

## Dilated Neighborhood Attention Transformer
*source: http://arxiv.org/abs/2209.15001v3*

| generator | mode | D1 | D2 | D3 | D4 | D5 | D6 | D7 | BSI | grounding_ratio | tag_coverage |
|---|---|---|---|---|---|---|---|---|---|---|---|
| mock | raw | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.125 | 0.500 | 0.435 | 1.000 | 0.000 |
| mock | bsi | 1.000 | 1.000 | 0.852 | 0.190 | 0.885 | 0.250 | 1.000 | 0.762 | 1.000 | 0.143 |
| openrouter | raw | 1.000 | 1.000 | 0.000 | 0.594 | 0.000 | 0.250 | 0.500 | 0.546 | 1.000 | 0.000 |
| openrouter | bsi | 0.242 | 1.000 | 0.000 | 0.888 | 0.000 | 0.500 | 0.500 | 0.449 | 1.000 | 0.000 |

## Music Transformer
*source: http://arxiv.org/abs/1809.04281v3*

| generator | mode | D1 | D2 | D3 | D4 | D5 | D6 | D7 | BSI | grounding_ratio | tag_coverage |
|---|---|---|---|---|---|---|---|---|---|---|---|
| mock | raw | 1.000 | 1.000 | 0.000 | 0.000 | 0.658 | 0.250 | 1.000 | 0.549 | 1.000 | 0.000 |
| mock | bsi | 1.000 | 1.000 | 0.768 | 0.206 | 1.000 | 0.250 | 1.000 | 0.763 | 1.000 | 0.200 |
| openrouter | raw | 1.000 | 1.000 | 0.000 | 0.613 | 0.000 | 0.250 | 1.000 | 0.574 | 1.000 | 0.000 |
| openrouter | bsi | 0.371 | 1.000 | 0.000 | 0.927 | 0.000 | 0.500 | 0.000 | 0.459 | 1.000 | 0.000 |

## Déjà vu: A Contextualized Temporal Attention Mechanism for Sequential Recommendation
*source: http://arxiv.org/abs/2002.00741v1*

| generator | mode | D1 | D2 | D3 | D4 | D5 | D6 | D7 | BSI | grounding_ratio | tag_coverage |
|---|---|---|---|---|---|---|---|---|---|---|---|
| mock | raw | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.250 | 0.500 | 0.445 | 1.000 | 0.000 |
| mock | bsi | 1.000 | 1.000 | 0.730 | 0.224 | 1.000 | 0.375 | 1.000 | 0.769 | 1.000 | 0.375 |
| openrouter | raw | 1.000 | 1.000 | 0.000 | 0.743 | 0.317 | 0.375 | 1.000 | 0.644 | 1.000 | 0.000 |
| openrouter | bsi | 0.111 | 1.000 | 0.000 | 0.938 | 0.000 | 0.625 | 0.500 | 0.439 | 1.000 | 0.000 |

## Energy-Gated Attention and Wavelet Positional Encoding: Complementary Inductive Biases for Transformer Attention
*source: http://arxiv.org/abs/2605.26355v1*

| generator | mode | D1 | D2 | D3 | D4 | D5 | D6 | D7 | BSI | grounding_ratio | tag_coverage |
|---|---|---|---|---|---|---|---|---|---|---|---|
| mock | raw | 0.626 | 1.000 | 0.000 | 0.000 | 0.469 | 0.000 | 0.500 | 0.399 | 1.000 | 0.000 |
| mock | bsi | 1.000 | 1.000 | 0.890 | 0.164 | 1.000 | 0.125 | 1.000 | 0.768 | 1.000 | 0.200 |
| openrouter | raw | 1.000 | 1.000 | 0.000 | 0.460 | 0.352 | 0.125 | 0.500 | 0.555 | 1.000 | 0.000 |
| openrouter | bsi | 0.137 | 1.000 | 0.000 | 0.927 | 0.000 | 0.625 | 0.500 | 0.443 | 1.000 | 0.000 |
