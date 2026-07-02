"""
AnalyzedDataset: a collection of (raw article, BSI analysis text) pairs.

This is the input format for BSIEvaluator's "compare raw vs analyzed"
scoring. Since this benchmark runner cannot itself call an LLM to produce
BSI analyses (no network access here), the analysis text is expected to be
pasted in from a real BSI run (Termux, claude.ai, the deployed API, etc.)
and saved to a JSON file matching the schema below, then loaded with
`AnalyzedDatasetIO.load()`.

JSON schema:
{
  "name": "optional label for this batch",
  "items": [
    {
      "article": {"title": ..., "abstract": ..., "doi": ..., "url": ...},
      "analysis": {"text": ..., "source_model": ..., "generated_at": ...}
    },
    ...
  ]
}
"""

import json
from dataclasses import dataclass, field, asdict

from bsi_benchmark.models.article import Article
from bsi_benchmark.models.analysis import Analysis
from bsi_benchmark.models.analyzed_article import AnalyzedArticle


@dataclass
class AnalyzedDataset:
    name: str = "unnamed"
    items: list[AnalyzedArticle] = field(default_factory=list)

    @property
    def size(self) -> int:
        return len(self.items)


class AnalyzedDatasetIO:

    def save(self, dataset: AnalyzedDataset, filename: str) -> None:
        payload = {
            "name": dataset.name,
            "items": [
                {
                    "article": asdict(item.article),
                    "analysis": asdict(item.analysis),
                }
                for item in dataset.items
            ],
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

    def load(self, filename: str) -> AnalyzedDataset:
        with open(filename, encoding="utf-8") as f:
            data = json.load(f)

        items = [
            AnalyzedArticle(
                article=Article(**entry["article"]),
                analysis=Analysis(**entry["analysis"]),
            )
            for entry in data["items"]
        ]

        return AnalyzedDataset(name=data.get("name", "unnamed"), items=items)
