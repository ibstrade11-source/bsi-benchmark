from dataclasses import dataclass


@dataclass
class ExecutionContext:
    mode: str = "offline"
