import json
from dataclasses import asdict

from bsi_benchmark.models.article import Article

from .dataset import Dataset


class DatasetIO:

    def save(self, dataset, filename):

        with open(filename, "w", encoding="utf-8") as f:

            json.dump(
                asdict(dataset),
                f,
                indent=2,
                ensure_ascii=False,
            )

    def load(self, filename):

        with open(filename, encoding="utf-8") as f:

            data = json.load(f)

        articles = [
            Article(**a)
            for a in data["articles"]
        ]

        return Dataset(
            provider=data["provider"],
            query=data["query"],
            articles=articles,
        )
