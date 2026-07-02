from dataclasses import dataclass

# Official BIO v1.0 weights (from the BSI master repository), applied to
# the weighted total below. Previously this was an unweighted mean of the
# seven dimensions, which did not match the documented BSI_linear formula:
#   BSI_linear = sum(w_i * D_i)
WEIGHTS = {
    "d1": 0.22,  # ConditionalDepth
    "d2": 0.18,  # LongitudinalCoherence
    "d3": 0.18,  # AuthenticEthicalLayer
    "d4": 0.17,  # CreativeValueAdd
    "d5": 0.12,  # StrategicDepth
    "d6": 0.08,  # InterdisciplinaryBreadth
    "d7": 0.05,  # AntiPerformativeDrift
}

assert abs(sum(WEIGHTS.values()) - 1.0) < 1e-9, "BSI weights must sum to 1.0"


@dataclass
class BSIDimensions:
    d1: float  # ConditionalDepth         (proxy: conditional-reasoning density)
    d2: float  # LongitudinalCoherence    (proxy: tag/language coherence)
    d3: float  # AuthenticEthicalLayer    (proxy: Meta-layer depth)
    d4: float  # CreativeValueAdd         (proxy: lexical novelty vs source)
    d5: float  # StrategicDepth           (proxy: implication-statement density)
    d6: float  # InterdisciplinaryBreadth (proxy: distinct domain clusters)
    d7: float  # AntiPerformativeDrift    (proxy: hedge-vs-overclaim balance)

    @property
    def total(self) -> float:
        return sum(
            getattr(self, dim) * weight
            for dim, weight in WEIGHTS.items()
        )
