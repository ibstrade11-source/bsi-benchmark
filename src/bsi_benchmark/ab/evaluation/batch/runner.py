from bsi_benchmark.ab.client import BSIApiClient


class ABBatchRunner:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.api = BSIApiClient(base_url)

    def run(self, dataset):
        results = []

        for item in dataset:
            text = item["text"]

            baseline = self.api.analyze(text)
            with_bsi = self.api.score(text, detail=True)

            results.append({
                "text": text,
                "baseline": baseline,
                "with_bsi": with_bsi,
            })

        return results
