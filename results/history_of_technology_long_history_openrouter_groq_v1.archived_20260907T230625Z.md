# Comparison: A Long History: From Universal Language to Artificial Intelligence

## Run metadata
- bsi-benchmark version: 0.1.0
- git commit: 89a941006de1ccab30f7a16e09f86841cd5991eb
- run timestamp (UTC): 2026-09-07T23:02:58Z
- methodology: Scores/judgements come from an independent LLM judge (see comparison/judge.py) instructed not to reuse BSI's own D1-D7/EIG vocabulary and to choose its own evaluation criteria. If no judge model is available or its response cannot be parsed, the run falls back to a simple keyword-presence heuristic -- the stored record's own 'criteria_source' field ('llm' vs 'heuristic_fallback') always says honestly which one produced a given result. Neither path is a validated measurement of analytical quality until checked against independent human judgement on a representative sample.

> BSI prompt source: https://github.com/ibstrade11-source/behmanesh-index-prompt/blob/main/MASTER_PROMPT_BSI_v3.4.2.md

## Benchmark status

- status: **benchmarkable**

## Retrieval validation

- retrieval status: **accepted**
- query type: title
- selected title: A Long History: From Universal Language to Artificial Intelligence
- selected candidate rank: 1
- title match score: 1.0
- acceptance threshold: 0.72
- rejected candidates: 0

## A Long History: From Universal Language to Artificial Intelligence

*source:* https://openalex.org/W7160269223
*doi:* https://doi.org/10.1353/tech.2026.a988849

### Generation failures

- **openrouter/bsi**: OpenRouter response did not contain a non-empty 'choices' array. keys=['id', 'error']; error={'message': 'Upstream error from Nvidia: Service temporarily overloaded', 'code': 502}; body_prefix='{"id":"gen-1788822325-65Cobx3EY7xvLumuiGaE","error":{"message":"Upstream error from Nvidia: Service temporarily overloaded","code":502}}'

### Judge Evaluation

No judge result.
