from bsi_benchmark.ab.client import BSIApiClient
from .prompts import build_baseline_prompt, build_bsi_prompt


class ABEvaluationEngine:

    def __init__(self, client=None):
        self.client = client or BSIApiClient()

    def run(self, query: str):

        baseline_prompt = build_baseline_prompt(query)
        bsi_prompt = build_bsi_prompt(query)

        baseline_result = self.client.score(baseline_prompt)
        bsi_result = self.client.score(bsi_prompt)

        return {
            "query": query,

            "baseline": {
                "score": baseline_result["bsi_score"],
                "eig": baseline_result["eig_score"],
                "interpretation": baseline_result["interpretation"],
            },

            "bsi_enhanced": {
                "score": bsi_result["bsi_score"],
                "eig": bsi_result["eig_score"],
                "interpretation": bsi_result["interpretation"],
            },

            "delta": {
                "bsi_improvement": round(
                    bsi_result["bsi_score"] - baseline_result["bsi_score"], 4
                ),
                "eig_change": round(
                    bsi_result["eig_score"] - baseline_result["eig_score"], 4
                ),
            }
        }
