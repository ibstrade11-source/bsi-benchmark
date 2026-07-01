from dataclasses import dataclass


@dataclass
class BenchmarkResult:
    dataset: object
    evaluation: object
    report: str
