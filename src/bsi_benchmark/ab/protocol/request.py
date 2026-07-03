from dataclasses import dataclass


@dataclass(slots=True)
class ABRequest:
    provider: str
    query: str
    use_bsi: bool = False
    detail: bool = False
