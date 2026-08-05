# Comparison: transformer attention mechanism

## Run metadata
- bsi-benchmark version: 0.1.0
- git commit: 6ca74058de582d7baa7334af0a164f48fcef2b82 (uncommitted local changes present)
- run timestamp (UTC): 2026-08-05T04:00:47Z
- methodology note: Scores are produced by BSIEvaluator, an offline lexical/keyword-based proxy for the seven BIO v1.0 dimensions (regex and keyword matching, not semantic understanding). They are first-pass triage signals, not a validated measurement of analytical quality, until checked against independent human judgement on a representative sample. Do not cite numeric BSI scores as a certified metric without that validation step.

> BSI prompt source (read it yourself, unedited): https://github.com/ibstrade11-source/behmanesh-index-prompt/blob/main/MASTER_PROMPT_BSI_v3.4.2.md

## Transformer-based Personalized Attention Mechanism for Medical Images with Clinical Records
*source: http://arxiv.org/abs/2206.03003v2*

| generator | mode | D1 | D2 | D3 | D4 | D5 | D6 | D7 | BSI | grounding_ratio | tag_coverage |
|---|---|---|---|---|---|---|---|---|---|---|---|
| openrouter | raw | 1.000 | 1.000 | 0.000 | 0.732 | 0.000 | 0.250 | 0.500 | 0.570 | 1.000 | 0.000 |
| openrouter | bsi | ERROR: Could not parse OpenRouter response: 'choices' |

## Dilated Neighborhood Attention Transformer
*source: http://arxiv.org/abs/2209.15001v3*

| generator | mode | D1 | D2 | D3 | D4 | D5 | D6 | D7 | BSI | grounding_ratio | tag_coverage |
|---|---|---|---|---|---|---|---|---|---|---|---|
| openrouter | raw | 0.735 | 1.000 | 0.000 | 0.639 | 0.000 | 0.250 | 1.000 | 0.520 | 1.000 | 0.000 |
| openrouter | bsi | 0.296 | 1.000 | 1.000 | 0.866 | 0.000 | 0.250 | 1.000 | 0.642 | 1.000 | 0.000 |

## Music Transformer
*source: http://arxiv.org/abs/1809.04281v3*

| generator | mode | D1 | D2 | D3 | D4 | D5 | D6 | D7 | BSI | grounding_ratio | tag_coverage |
|---|---|---|---|---|---|---|---|---|---|---|---|
| openrouter | raw | 1.000 | 1.000 | 0.000 | 0.648 | 0.000 | 0.250 | 0.500 | 0.555 | 1.000 | 0.000 |
| openrouter | bsi | 0.377 | 1.000 | 0.000 | 0.932 | 0.000 | 0.625 | 0.500 | 0.497 | 1.000 | 0.000 |

## Déjà vu: A Contextualized Temporal Attention Mechanism for Sequential Recommendation
*source: http://arxiv.org/abs/2002.00741v1*

| generator | mode | D1 | D2 | D3 | D4 | D5 | D6 | D7 | BSI | grounding_ratio | tag_coverage |
|---|---|---|---|---|---|---|---|---|---|---|---|
| openrouter | raw | 1.000 | 1.000 | 0.000 | 0.697 | 0.000 | 0.375 | 1.000 | 0.599 | 1.000 | 0.000 |
| openrouter | bsi | 0.304 | 1.000 | 0.000 | 0.940 | 0.000 | 0.625 | 0.500 | 0.482 | 1.000 | 0.000 |

## Energy-Gated Attention and Wavelet Positional Encoding: Complementary Inductive Biases for Transformer Attention
*source: http://arxiv.org/abs/2605.26355v1*

| generator | mode | D1 | D2 | D3 | D4 | D5 | D6 | D7 | BSI | grounding_ratio | tag_coverage |
|---|---|---|---|---|---|---|---|---|---|---|---|
| openrouter | raw | 0.984 | 1.000 | 0.000 | 0.489 | 0.369 | 0.250 | 0.500 | 0.569 | 1.000 | 0.000 |
| openrouter | bsi | 0.114 | 1.000 | 0.000 | 0.899 | 0.000 | 0.500 | 0.500 | 0.423 | 1.000 | 0.000 |
