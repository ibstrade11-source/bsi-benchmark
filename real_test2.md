# Comparison: machine learning

## machine learning

| generator | mode | D1 | D2 | D3 | D4 | D5 | D6 | D7 | BSI | grounding_ratio | tag_coverage |
|---|---|---|---|---|---|---|---|---|---|---|---|
| mock | raw | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.500 | 0.205 | 1.000 | 0.000 |
| mock | bsi | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.500 | 0.205 | 1.000 | 0.000 |
| anthropic | raw | ERROR: Anthropic HTTP 400: {"type":"error","error":{"type":"invalid_request_error","message":"Your credit balance is too low to access the Anthropic API. Please go to Plans & Billing to upgrade or purchase credits."},"request_id":"req_011CcfbA9TZEFqCyWMahCZLD"} |
| anthropic | bsi | ERROR: Anthropic HTTP 400: {"type":"error","error":{"type":"invalid_request_error","message":"Your credit balance is too low to access the Anthropic API. Please go to Plans & Billing to upgrade or purchase credits."},"request_id":"req_011CcfbAB827HD5w43Rsa2ch"} |
