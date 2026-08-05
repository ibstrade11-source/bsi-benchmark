"""
ComparisonSpec: configuration for a benchmark run.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class ComparisonSpec:
    generators: List[str]
    prompt_modes: Dict[str, str] = field(default_factory=dict)

    # Optional independent judge model used for raw vs BSI comparison.
    judge: Optional[str] = None
