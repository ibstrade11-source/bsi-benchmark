from dataclasses import dataclass


@dataclass(slots=True)
class BenchmarkConfig:
    provider: str
    evaluator: str
    reporter: str
