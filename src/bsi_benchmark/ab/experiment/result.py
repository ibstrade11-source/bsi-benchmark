from dataclasses import dataclass


@dataclass(slots=True)
class ExperimentResult:
    prompt: str
    baseline: str
    treatment: str
