import json


class JsonExporter:

    def export(self, result, path):
        data = {
            "provider": result.dataset.provider,
            "query": result.dataset.query,
            "articles": len(result.dataset.articles),
            "scores": result.evaluation.scores,
        }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
