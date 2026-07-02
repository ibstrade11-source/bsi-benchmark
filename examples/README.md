# Examples

## `sample_analyzed_dataset.json`
A minimal example of the AnalyzedDataset JSON schema consumed by:
```
bsi-benchmark evaluate --input examples/sample_analyzed_dataset.json
```
Use this shape when you already have a BSI analysis (e.g. pasted from a
real BSI run in Termux or claude.ai) and just want it scored, without
calling any LLM API from this tool.

## `sample_bsi_prompt.txt`
A placeholder BSI prompt template ({title}/{abstract} placeholders) for
smoke-testing `compare`. **Replace this with your actual
MASTER_PROMPT_BSI_v3.4.2.md content** (or a copy of it) before running a
real benchmark -- this file is intentionally NOT the real BSI prompt, it's
just enough structure for the mock generator / your own testing to exercise
the "bsi" prompt-mode branch.

## Try it fully offline (no API keys needed)
```
bsi-benchmark compare \
  --provider mock --query "test" \
  --generators mock \
  --bsi-prompt-file examples/sample_bsi_prompt.txt \
  --output /tmp/demo
```

## Try it with a real model (requires ANTHROPIC_API_KEY / OPENAI_API_KEY)
```
export ANTHROPIC_API_KEY=...
bsi-benchmark compare \
  --provider crossref --query "labor economics import competition" \
  --generators anthropic \
  --bsi-prompt-file /path/to/MASTER_PROMPT_BSI_v3.4.2.md \
  --output /tmp/real_run
```
