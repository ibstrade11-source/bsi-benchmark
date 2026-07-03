# Comparison: machine learning

## machine learning

| generator | mode | D1 | D2 | D3 | D4 | D5 | D6 | D7 | BSI | grounding_ratio | tag_coverage |
|---|---|---|---|---|---|---|---|---|---|---|---|
| mock | raw | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.500 | 0.205 | 1.000 | 0.000 |
| mock | bsi | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.500 | 0.205 | 1.000 | 0.000 |
| anthropic | raw | ERROR: Anthropic HTTP 401: {"type":"error","error":{"type":"authentication_error","message":"invalid x-api-key"},"request_id":"req_011CcfaFadQhgNRjs1XZqTzr"} |
| anthropic | bsi | ERROR: Anthropic HTTP 401: {"type":"error","error":{"type":"authentication_error","message":"invalid x-api-key"},"request_id":"req_011CcfaFdy5WYG1cvPDj2ZJv"} |
