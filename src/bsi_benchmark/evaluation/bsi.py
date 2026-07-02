"""
BSIEvaluator: scores a *BSI-generated analysis* against the raw article it
was produced from.

Previous version (fixed): this evaluator scored properties of the fetched
article metadata itself (article count, presence of abstract/DOI, title
length) and mislabeled those as the seven BIO v1.0 dimensions -- three of
the seven fields were literal duplicates of the other three (d4=d1, d5=d2,
d6=d3), and the total was an unweighted mean rather than the documented
weighted BSI_linear formula. That measured "how complete is the fetched
bibliographic record", not "how good is the BSI analysis of it".

This version takes an AnalyzedArticle (raw Article + Analysis.text) and
scores the *analysis text* using independent lexical proxies for each
dimension, defined in text_analysis.py. Every one of the seven scores below
is computed from a different underlying signal -- there is no duplication.

These are still heuristic proxies, not a full re-implementation of BSI's
own reasoning (that would require an LLM, which this offline benchmark
runner does not call). See text_analysis.py docstring for the honesty
caveat on what these numbers do and don't mean. Two additional diagnostic
signals (grounding_ratio, tag_coverage) are reported alongside the seven
weighted dimensions but are NOT folded into the weighted total, since they
don't map cleanly onto a single BIO dimension -- they are closer to an EIG
Claim-Evidence proxy and a tagging-discipline proxy respectively.
"""

from .dimensions import BSIDimensions
from .text_analysis import analyze_text, lexical_novelty, DOMAIN_CLUSTERS
from .result import EvaluationResult

# Saturation constants: density above these thresholds is treated as a
# "full score" of 1.0 for that dimension. These are deliberately rough and
# should be recalibrated once real BSI output samples are run through this
# evaluator and the resulting scores are checked against human judgement.
CONDITIONAL_SATURATION_PER_100_WORDS = 1.5
IMPLICATION_SATURATION_PER_100_WORDS = 1.0


def _density_score(count: int, word_count: int, saturation_per_100: float) -> float:
    if word_count == 0:
        return 0.0
    per_100 = (count / word_count) * 100
    return min(per_100 / saturation_per_100, 1.0)


def _meta_layer_depth_score(layers_present: set, word_count: int) -> float:
    if "meta" not in layers_present:
        return 0.0
    if word_count == 0:
        return 0.0
    # Reward having a Meta layer at all (0.4 baseline) plus a graded bonus
    # for it being a substantial section rather than a bare header. We
    # don't have per-layer word counts without a layer-aware splitter, so
    # this uses overall analysis length as a crude proxy for "there's
    # probably substance here", capped so a merely-long analysis with a
    # token Meta header doesn't max out the score.
    length_bonus = min(word_count / 300.0, 1.0) * 0.6
    return 0.4 + length_bonus


def _anti_overclaim_score(hedge_count: int, overclaim_count: int) -> float:
    # 1.0 = no overclaiming relative to hedging; 0.0 = only overclaiming,
    # no hedging at all. A text with neither marker scores neutral (0.5)
    # rather than a perfect 1.0, since "never signals certainty either way"
    # is not the same as "demonstrably calibrated".
    total = hedge_count + overclaim_count
    if total == 0:
        return 0.5
    return hedge_count / total


class BSIEvaluator:

    name = "bsi"

    def score_dimensions(self, analyzed_article) -> BSIDimensions:
        """
        Args:
            analyzed_article: a models.analyzed_article.AnalyzedArticle
                (raw Article + Analysis text pair).

        Returns the raw BSIDimensions (d1..d7 + weighted .total). Use
        `evaluate()` instead if you want the full result dict including
        the two diagnostic-only signals (grounding_ratio, tag_coverage).
        """
        analysis_text = analyzed_article.analysis.text or ""
        source_text = analyzed_article.source_text

        if not analysis_text.strip():
            return BSIDimensions(d1=0.0, d2=0.0, d3=0.0, d4=0.0, d5=0.0, d6=0.0, d7=0.0)

        signals = analyze_text(analysis_text, source_text)

        d1 = _density_score(
            signals.conditional_count, signals.word_count,
            CONDITIONAL_SATURATION_PER_100_WORDS,
        )
        d2 = signals.tag_language_coherence
        d3 = _meta_layer_depth_score(signals.layers_present, signals.word_count)
        d4 = lexical_novelty(analysis_text, source_text)
        d5 = _density_score(
            signals.implication_count, signals.word_count,
            IMPLICATION_SATURATION_PER_100_WORDS,
        )
        d6 = min(len(signals.domain_hits) / len(DOMAIN_CLUSTERS), 1.0)
        d7 = _anti_overclaim_score(signals.hedge_count, signals.overclaim_count)

        return BSIDimensions(d1=d1, d2=d2, d3=d3, d4=d4, d5=d5, d6=d6, d7=d7)

    def evaluate(self, analyzed_article) -> EvaluationResult:
        """
        Full result: weighted D1-D7 + BSI total + the two non-weighted
        diagnostic signals (grounding_ratio, tag_coverage). This is the
        method the evaluation registry/engine calls.
        """
        analysis_text = analyzed_article.analysis.text or ""
        source_text = analyzed_article.source_text

        dims = self.score_dimensions(analyzed_article)
        signals = analyze_text(analysis_text, source_text)

        scores = {
            "D1": dims.d1,
            "D2": dims.d2,
            "D3": dims.d3,
            "D4": dims.d4,
            "D5": dims.d5,
            "D6": dims.d6,
            "D7": dims.d7,
            "BSI": dims.total,
            "grounding_ratio": signals.grounding_ratio,
            "tag_coverage": signals.tag_coverage,
        }

        return EvaluationResult(evaluator="bsi", scores=scores)
