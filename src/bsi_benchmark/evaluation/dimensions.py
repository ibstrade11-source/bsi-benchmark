from dataclasses import dataclass


@dataclass
class BSIDimensions:
    d1: float
    d2: float
    d3: float
    d4: float
    d5: float
    d6: float
    d7: float

    @property
    def total(self) -> float:
        return (
            self.d1
            + self.d2
            + self.d3
            + self.d4
            + self.d5
            + self.d6
            + self.d7
        ) / 7.0
