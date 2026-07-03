def build_baseline_prompt(query: str) -> str:
    return f"""
You are a research assistant.
Answer the following query:

{query}
"""


def build_bsi_prompt(query: str) -> str:
    return f"""
You are a research assistant enhanced with the BSI framework.

You MUST:
- reason structurally
- separate facts from assumptions
- avoid hallucination
- show epistemic uncertainty

Query:
{query}
"""
