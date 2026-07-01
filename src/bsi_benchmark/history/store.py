import json
from pathlib import Path
from datetime import datetime


class HistoryStore:

    def __init__(self, directory="reports/history"):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

    def save(self, result):

        filename = datetime.utcnow().strftime("%Y%m%d-%H%M%S.json")

        path = self.directory / filename

        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "provider": result.dataset.provider,
                    "query": result.dataset.query,
                    "scores": result.evaluation.scores,
                },
                f,
                indent=2,
                ensure_ascii=False,
            )

        return path
