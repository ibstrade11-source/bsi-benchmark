"""
Load/save SelfComparisonRecord as JSON.

Input schema expected from an analyst (see
examples/self_compare_example.json for a filled-in sample and
examples/self_compare_prompt.md for the instructions given to the
analyst):

{
  "article": {"title": "...", "doi": "...", "url": "..."},
  "analyst_model": "claude-sonnet-5",
  "criteria_rationale": "free text: why I chose these criteria",
  "criteria": [
    {"criterion": "...", "raw_score": 6, "bsi_score": 8, "notes": "..."},
    ...
  ],
  "overall_winner": "bsi",
  "overall_reasoning": "free text"
}

"doi"/"url" on the article are optional. "overall_winner" is stored as
given by the analyst (not re-derived), since it is a holistic judgement
that need not mechanically follow from the per-criterion table -- unlike
the per-criterion winner, which IS derived (see models.CriterionScore).
"""
from __future__ import annotations

import json
from dataclasses import asdict

from .models import CriterionScore, SelfComparisonRecord


class SelfComparisonIO:

    def load(self, path: str) -> SelfComparisonRecord:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        try:
            article = data["article"]
            criteria_raw = data["criteria"]
        except KeyError as e:
            raise ValueError(
                f"self-compare input missing required key: {e}. "
                "Expected top-level keys: article, analyst_model, criteria, "
                "overall_winner, overall_reasoning. See "
                "examples/self_compare_example.json for the expected shape."
            ) from e

        if not criteria_raw:
            raise ValueError(
                "self-compare input has an empty 'criteria' list -- at "
                "least one analyst-chosen criterion with raw_score and "
                "bsi_score is required."
            )

        criteria = []
        for i, c in enumerate(criteria_raw):
            try:
                criteria.append(CriterionScore(
                    criterion=c["criterion"],
                    raw_score=float(c["raw_score"]),
                    bsi_score=float(c["bsi_score"]),
                    notes=c.get("notes"),
                ))
            except KeyError as e:
                raise ValueError(
                    f"criteria[{i}] missing required key: {e}. Each "
                    "criterion needs 'criterion', 'raw_score', 'bsi_score'."
                ) from e

        return SelfComparisonRecord(
            article_title=article.get("title", "(untitled)"),
            article_doi=article.get("doi"),
            article_url=article.get("url"),
            analyst_model=data.get("analyst_model", "unknown"),
            criteria=criteria,
            overall_winner=data.get("overall_winner", "unspecified"),
            overall_reasoning=data.get("overall_reasoning", ""),
            criteria_rationale=data.get("criteria_rationale"),
            run_metadata=data.get("run_metadata"),
        )

    def save(self, record: SelfComparisonRecord, path: str) -> None:
        payload = {
            "article": {
                "title": record.article_title,
                "doi": record.article_doi,
                "url": record.article_url,
            },
            "analyst_model": record.analyst_model,
            "criteria_rationale": record.criteria_rationale,
            "criteria": [
                {
                    "criterion": c.criterion,
                    "raw_score": c.raw_score,
                    "bsi_score": c.bsi_score,
                    "winner": c.winner,
                    "notes": c.notes,
                }
                for c in record.criteria
            ],
            "overall_winner": record.overall_winner,
            "overall_reasoning": record.overall_reasoning,
            "summary": {
                "raw_wins": record.raw_wins(),
                "bsi_wins": record.bsi_wins(),
                "ties": record.ties(),
            },
            "run_metadata": record.run_metadata,
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
