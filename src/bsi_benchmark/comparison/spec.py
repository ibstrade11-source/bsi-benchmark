"""
ComparisonSpec: what to run.

generators: names registered in generation.registry (e.g. ["anthropic",
    "openai", "mock"]).
prompt_modes: label -> prompt template string. Typical usage is two modes,
    e.g. {"raw": "<plain instruction>", "bsi": "<full BSI master prompt>"},
    so the resulting report directly answers "does BSI-guided analysis
    score higher than baseline analysis, and does that hold across
    models?" -- which is the comparison this whole project exists to make
    automatic and repeatable instead of done by hand in a chat window.
"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class ComparisonSpec:
    generators: List[str]
    prompt_modes: Dict[str, str] = field(default_factory=dict)
