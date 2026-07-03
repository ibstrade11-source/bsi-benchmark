# Comparison: large language models

## Enhancing Human-Like Responses in Large Language Models

| generator | mode | D1 | D2 | D3 | D4 | D5 | D6 | D7 | BSI | grounding_ratio | tag_coverage |
|---|---|---|---|---|---|---|---|---|---|---|---|
| mock | raw | 0.833 | 1.000 | 0.000 | 0.000 | 1.000 | 0.250 | 0.500 | 0.528 | 1.000 | 0.000 |
| mock | bsi | 0.833 | 1.000 | 0.000 | 0.000 | 1.000 | 0.250 | 0.500 | 0.528 | 1.000 | 0.000 |
| anthropic | raw | ERROR: Anthropic HTTP 400: {"type":"error","error":{"type":"invalid_request_error","message":"Your credit balance is too low to access the Anthropic API. Please go to Plans & Billing to upgrade or purchase credits."},"request_id":"req_011CcfbKiQTKCQoaEMT5itAt"} |
| anthropic | bsi | ERROR: Anthropic HTTP 400: {"type":"error","error":{"type":"invalid_request_error","message":"Your credit balance is too low to access the Anthropic API. Please go to Plans & Billing to upgrade or purchase credits."},"request_id":"req_011CcfbKk8PdfDw6ptFyxJG4"} |

## Is Self-knowledge and Action Consistent or Not: Investigating Large Language Model's Personality

| generator | mode | D1 | D2 | D3 | D4 | D5 | D6 | D7 | BSI | grounding_ratio | tag_coverage |
|---|---|---|---|---|---|---|---|---|---|---|---|
| mock | raw | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.125 | 0.500 | 0.215 | 1.000 | 0.000 |
| mock | bsi | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.125 | 0.500 | 0.215 | 1.000 | 0.000 |
| anthropic | raw | ERROR: Anthropic HTTP 400: {"type":"error","error":{"type":"invalid_request_error","message":"Your credit balance is too low to access the Anthropic API. Please go to Plans & Billing to upgrade or purchase credits."},"request_id":"req_011CcfbKoSpHNjfi4DUtuzAS"} |
| anthropic | bsi | ERROR: Anthropic HTTP 400: {"type":"error","error":{"type":"invalid_request_error","message":"Your credit balance is too low to access the Anthropic API. Please go to Plans & Billing to upgrade or purchase credits."},"request_id":"req_011CcfbKq3ZXdeyCVyP3emb7"} |

## Large Language Models Lack Understanding of Character Composition of Words

| generator | mode | D1 | D2 | D3 | D4 | D5 | D6 | D7 | BSI | grounding_ratio | tag_coverage |
|---|---|---|---|---|---|---|---|---|---|---|---|
| mock | raw | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.125 | 0.500 | 0.215 | 1.000 | 0.000 |
| mock | bsi | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.125 | 0.500 | 0.215 | 1.000 | 0.000 |
| anthropic | raw | ERROR: Anthropic HTTP 400: {"type":"error","error":{"type":"invalid_request_error","message":"Your credit balance is too low to access the Anthropic API. Please go to Plans & Billing to upgrade or purchase credits."},"request_id":"req_011CcfbKtMFJSXVWkNTrgU2i"} |
| anthropic | bsi | ERROR: Anthropic HTTP 400: {"type":"error","error":{"type":"invalid_request_error","message":"Your credit balance is too low to access the Anthropic API. Please go to Plans & Billing to upgrade or purchase credits."},"request_id":"req_011CcfbL9zpzLkxSQ2X73v8u"} |

## Unmasking the Shadows of AI: Investigating Deceptive Capabilities in Large Language Models

| generator | mode | D1 | D2 | D3 | D4 | D5 | D6 | D7 | BSI | grounding_ratio | tag_coverage |
|---|---|---|---|---|---|---|---|---|---|---|---|
| mock | raw | 1.000 | 1.000 | 0.000 | 0.000 | 1.000 | 0.250 | 0.500 | 0.565 | 1.000 | 0.000 |
| mock | bsi | 1.000 | 1.000 | 0.000 | 0.000 | 1.000 | 0.250 | 0.500 | 0.565 | 1.000 | 0.000 |
| anthropic | raw | ERROR: Anthropic HTTP 400: {"type":"error","error":{"type":"invalid_request_error","message":"Your credit balance is too low to access the Anthropic API. Please go to Plans & Billing to upgrade or purchase credits."},"request_id":"req_011CcfbLF7AJQzPiU9NdVgzf"} |
| anthropic | bsi | ERROR: Anthropic HTTP 400: {"type":"error","error":{"type":"invalid_request_error","message":"Your credit balance is too low to access the Anthropic API. Please go to Plans & Billing to upgrade or purchase credits."},"request_id":"req_011CcfbLL9GmzSoGuEp54gW2"} |

## Self-Cognition in Large Language Models: An Exploratory Study

| generator | mode | D1 | D2 | D3 | D4 | D5 | D6 | D7 | BSI | grounding_ratio | tag_coverage |
|---|---|---|---|---|---|---|---|---|---|---|---|
| mock | raw | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.125 | 0.500 | 0.435 | 1.000 | 0.000 |
| mock | bsi | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.125 | 0.500 | 0.435 | 1.000 | 0.000 |
| anthropic | raw | ERROR: Anthropic HTTP 400: {"type":"error","error":{"type":"invalid_request_error","message":"Your credit balance is too low to access the Anthropic API. Please go to Plans & Billing to upgrade or purchase credits."},"request_id":"req_011CcfbLRJLVR7GeTrdg1Heu"} |
| anthropic | bsi | ERROR: Anthropic HTTP 400: {"type":"error","error":{"type":"invalid_request_error","message":"Your credit balance is too low to access the Anthropic API. Please go to Plans & Billing to upgrade or purchase credits."},"request_id":"req_011CcfbLWYr3qaGjuV5Eim3X"} |
