import json

from bsi_benchmark.models.analysis import Analysis


class LLMJudge:
    """
    Independent LLM judge for raw vs BSI comparison.
    Judge creates its own criteria and scores both analyses.
    """

    def __init__(self, generator):
        self.generator = generator

    def compare(self, article, raw_analysis: Analysis, bsi_analysis: Analysis):

        output_schema = {
            "winner": "raw|bsi|tie",
            "criteria": [
                {
                    "name": "criterion name",
                    "importance": 0,
                    "raw_score": 0,
                    "bsi_score": 0,
                    "reason": ""
                }
            ],
            "total_scores": {
                "raw": 0,
                "bsi": 0
            },
            "reasoning": ""
        }

        prompt = f"""
You are an independent scientific judge.

Compare two analyses of the same article.

Article:
{article.title}

RAW ANALYSIS:
{raw_analysis.text}

BSI ANALYSIS:
{bsi_analysis.text}

Rules:

1. Create your own evaluation criteria.
2. Do not use predefined criteria.
3. Score each criterion for both analyses from 0 to 10.
4. Select the winner.
5. Explain your reasoning.

Return ONLY valid JSON.

Required structure:

{json.dumps(output_schema, indent=2)}
"""

        result = self.generator.generate_raw(article, prompt)

        try:
            return json.loads(result.text)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {
                "winner": "unknown",
                "raw": result.text,
                "error": str(e)
            }
