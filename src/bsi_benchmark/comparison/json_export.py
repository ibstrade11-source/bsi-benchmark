"""
JSON export of a ComparisonReport, for feeding into further statistical
analysis (e.g. the research-edition claim-registry / statistical-analysis
work already scaffolded in the main BSI monograph repo) rather than only
reading the markdown table by eye.
"""

import json
from dataclasses import asdict

from .result import ComparisonReport


def to_dict(report: ComparisonReport) -> dict:
    return asdict(report)


def save(report: ComparisonReport, path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(to_dict(report), f, indent=2, ensure_ascii=False)
