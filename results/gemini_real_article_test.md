# Comparison: transformer attention mechanism

## Run metadata
- bsi-benchmark version: 0.1.0
- git commit: 499f9642633cdccbb8d2b79fdbb16ddb0a03cbd2 (uncommitted local changes present)
- run timestamp (UTC): 2026-08-04T03:52:09Z
- methodology note: Scores are produced by BSIEvaluator, an offline lexical/keyword-based proxy for the seven BIO v1.0 dimensions (regex and keyword matching, not semantic understanding). They are first-pass triage signals, not a validated measurement of analytical quality, until checked against independent human judgement on a representative sample. Do not cite numeric BSI scores as a certified metric without that validation step.

> BSI prompt source (read it yourself, unedited): https://github.com/ibstrade11-source/behmanesh-index-prompt/blob/main/MASTER_PROMPT_BSI_v3.4.2.md

## Transformer-based Personalized Attention Mechanism for Medical Images with Clinical Records
*source: http://arxiv.org/abs/2206.03003v2*

| generator | mode | D1 | D2 | D3 | D4 | D5 | D6 | D7 | BSI | grounding_ratio | tag_coverage |
|---|---|---|---|---|---|---|---|---|---|---|---|
| mock | raw | 1.000 | 1.000 | 0.000 | 0.000 | 0.820 | 0.125 | 1.000 | 0.558 | 1.000 | 0.000 |
| mock | bsi | 1.000 | 1.000 | 0.708 | 0.264 | 1.000 | 0.125 | 1.000 | 0.752 | 1.000 | 0.273 |
| gemini | raw | 1.000 | 1.000 | 0.000 | 0.602 | 0.000 | 0.250 | 0.500 | 0.547 | 1.000 | 0.000 |
| gemini | bsi | 0.188 | 1.000 | 1.000 | 0.977 | 0.000 | 0.750 | 0.333 | 0.644 | 1.000 | 0.000 |

## Dilated Neighborhood Attention Transformer
*source: http://arxiv.org/abs/2209.15001v3*

| generator | mode | D1 | D2 | D3 | D4 | D5 | D6 | D7 | BSI | grounding_ratio | tag_coverage |
|---|---|---|---|---|---|---|---|---|---|---|---|
| mock | raw | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.125 | 0.500 | 0.435 | 1.000 | 0.000 |
| mock | bsi | 1.000 | 1.000 | 0.852 | 0.190 | 0.885 | 0.250 | 1.000 | 0.762 | 1.000 | 0.143 |
| gemini | raw | 0.349 | 1.000 | 0.000 | 0.425 | 0.000 | 0.125 | 0.500 | 0.364 | 1.000 | 0.000 |
| gemini | bsi | 0.294 | 1.000 | 1.000 | 0.958 | 0.000 | 0.500 | 1.000 | 0.678 | 1.000 | 0.000 |

## Music Transformer
*source: http://arxiv.org/abs/1809.04281v3*

| generator | mode | D1 | D2 | D3 | D4 | D5 | D6 | D7 | BSI | grounding_ratio | tag_coverage |
|---|---|---|---|---|---|---|---|---|---|---|---|
| mock | raw | 1.000 | 1.000 | 0.000 | 0.000 | 0.658 | 0.250 | 1.000 | 0.549 | 1.000 | 0.000 |
| mock | bsi | 1.000 | 1.000 | 0.768 | 0.206 | 1.000 | 0.250 | 1.000 | 0.763 | 1.000 | 0.200 |
| gemini | raw | 0.808 | 1.000 | 0.000 | 0.471 | 0.000 | 0.250 | 0.500 | 0.483 | 1.000 | 0.000 |
| gemini | bsi | 0.186 | 1.000 | 1.000 | 0.960 | 0.000 | 0.500 | 0.000 | 0.604 | 1.000 | 0.000 |

## Déjà vu: A Contextualized Temporal Attention Mechanism for Sequential Recommendation
*source: http://arxiv.org/abs/2002.00741v1*

| generator | mode | D1 | D2 | D3 | D4 | D5 | D6 | D7 | BSI | grounding_ratio | tag_coverage |
|---|---|---|---|---|---|---|---|---|---|---|---|
| mock | raw | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.250 | 0.500 | 0.445 | 1.000 | 0.000 |
| mock | bsi | 1.000 | 1.000 | 0.730 | 0.224 | 1.000 | 0.375 | 1.000 | 0.769 | 1.000 | 0.375 |
| gemini | raw | 0.419 | 1.000 | 0.000 | 0.491 | 0.000 | 0.250 | 0.500 | 0.401 | 1.000 | 0.000 |
| gemini | bsi | 0.134 | 1.000 | 1.000 | 0.966 | 0.000 | 0.750 | 0.667 | 0.647 | 1.000 | 0.000 |

## Energy-Gated Attention and Wavelet Positional Encoding: Complementary Inductive Biases for Transformer Attention
*source: http://arxiv.org/abs/2605.26355v1*

| generator | mode | D1 | D2 | D3 | D4 | D5 | D6 | D7 | BSI | grounding_ratio | tag_coverage |
|---|---|---|---|---|---|---|---|---|---|---|---|
| mock | raw | 0.626 | 1.000 | 0.000 | 0.000 | 0.469 | 0.000 | 0.500 | 0.399 | 1.000 | 0.000 |
| mock | bsi | 1.000 | 1.000 | 0.890 | 0.164 | 1.000 | 0.125 | 1.000 | 0.768 | 1.000 | 0.200 |
| gemini | raw | 0.553 | 1.000 | 0.000 | 0.465 | 0.415 | 0.125 | 0.500 | 0.466 | 1.000 | 0.000 |
| gemini | bsi | 0.312 | 1.000 | 1.000 | 0.942 | 0.000 | 0.625 | 0.667 | 0.672 | 1.000 | 0.000 |
