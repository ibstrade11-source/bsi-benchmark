from dataclasses import dataclass


@dataclass
class SuiteResult:
    name: str
    scenarios: list
