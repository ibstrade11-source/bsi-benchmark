"""
Lightweight, offline, regex/keyword-based text analysis utilities.

IMPORTANT HONESTY NOTE (read before trusting these numbers):
These functions are heuristic lexical proxies, not semantic understanding.
They approximate the *spirit* of each BSI dimension using signals that are
cheap to compute without a network call or an LLM (this benchmark runner has
no model access of its own). Each proxy is documented with what it actually
measures and where it can be fooled (e.g. an analysis could game the
"hedge ratio" score by sprinkling "may" everywhere without being genuinely
more careful). Treat scores from this module as a *first-pass triage signal*,
not a certified BSI score. A human (or a real BSI-capable model) should
review any output before treating it as ground truth.

Supports Persian and English keyword/marker lists side by side, since real
BSI usage is bilingual.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Claim tags: [FACT] / [INFERENCE] / [HYPOTHESIS] / [SPECULATION]
# ---------------------------------------------------------------------------

CLAIM_TAG_PATTERN = re.compile(r"\[(FACT|INFERENCE|HYPOTHESIS|SPECULATION)\]")

# ---------------------------------------------------------------------------
# Layer headers: Manifest / Latent / Meta (English + common Persian labels
# observed in real BSI output, e.g. "لایه Manifest (آشکار)")
# ---------------------------------------------------------------------------

LAYER_PATTERNS = {
    "manifest": re.compile(r"manifest|آشکار", re.IGNORECASE),
    "latent": re.compile(r"latent|پنهان", re.IGNORECASE),
    "meta": re.compile(r"\bmeta\b|فرا\b", re.IGNORECASE),
}

# ---------------------------------------------------------------------------
# Hedge / overclaim / conditional / implication marker lists (fa + en)
# ---------------------------------------------------------------------------

HEDGE_MARKERS = [
    "ممکن است", "احتمالا", "احتمالاً", "شاید", "به نظر می‌رسد", "به نظر میرسد",
    "می‌تواند", "میتواند", "تا حدی",
    "may", "might", "could", "suggests", "appears to", "likely",
    "possibly", "seems to", "tends to", "arguably",
]

OVERCLAIM_MARKERS = [
    "قطعا", "قطعاً", "همیشه", "هرگز", "ثابت می‌کند", "بدون شک", "قطعی",
    "certainly", "always", "never", "definitely", "proves", "undeniably",
    "unquestionably", "guarantees", "conclusively",
]

CONDITIONAL_MARKERS = [
    "اگر", "در صورتی که", "درصورتی‌که", "مشروط بر", "مشروط به", "به شرط",
    "if", "provided that", "assuming", "conditional on", "given that",
    "insofar as", "to the extent that",
]

IMPLICATION_MARKERS = [
    "پیامد", "دلالت", "نتیجه می‌شود", "درنتیجه", "این یعنی",
    "implication", "suggests that", "going forward", "future work",
    "this means that", "downstream effect", "follow-on",
]

# ---------------------------------------------------------------------------
# Disciplinary domain clusters, for a crude interdisciplinary-breadth signal
# ---------------------------------------------------------------------------

DOMAIN_CLUSTERS = {
    "economics": ["economic", "market", "price", "gdp", "inflation", "اقتصاد", "بازار", "قیمت"],
    "sociology": ["social", "society", "sociolog", "institution", "جامعه", "اجتماعی", "نهاد"],
    "philosophy": ["philosoph", "epistem", "ontolog", "ethic", "فلسف", "معرفت", "هستی‌شناس", "اخلاق"],
    "biology_medicine": ["biolog", "medic", "clinical", "gene", "زیست", "پزشک", "بالینی"],
    "computer_science": ["algorithm", "model", "neural", "computation", "software", "الگوریتم", "مدل", "نرم‌افزار"],
    "law": ["legal", "law", "regulation", "statute", "حقوق", "قانون", "مقررات"],
    "physics": ["physic", "quantum", "particle", "فیزیک", "کوانتوم"],
    "history": ["historical", "century", "empire", "تاریخ", "قرن", "امپراتور"],
}

_STOPWORDS = {
    "the", "a", "an", "of", "in", "on", "to", "and", "or", "is", "are", "was",
    "were", "be", "this", "that", "with", "as", "for", "by", "it", "its",
    "از", "به", "با", "در", "را", "که", "این", "آن", "است", "بود", "برای",
    "یک", "و", "یا", "هم", "تا", "می", "شود", "شد", "کرد", "دارد",
}

_WORD_RE = re.compile(r"[^\W\d_]+", re.UNICODE)


def _tokenize(text: str) -> list[str]:
    return [
        w.lower() for w in _WORD_RE.findall(text or "")
        if len(w) > 2 and w.lower() not in _STOPWORDS
    ]


def _sentences(text: str) -> list[str]:
    # Split on Persian/Latin sentence terminators and newlines.
    parts = re.split(r"[.\n؟!?]+", text or "")
    return [p.strip() for p in parts if p.strip()]


def _count_markers(text: str, markers: list[str]) -> int:
    lowered = (text or "").lower()
    return sum(lowered.count(m.lower()) for m in markers)


@dataclass
class TextSignals:
    word_count: int
    tagged_sentences: list[tuple[str, str]]  # (tag, sentence)
    tag_coverage: float          # fraction of sentences carrying a claim tag
    layers_present: set          # subset of {"manifest","latent","meta"}
    hedge_count: int
    overclaim_count: int
    conditional_count: int
    implication_count: int
    domain_hits: set             # subset of DOMAIN_CLUSTERS keys
    tag_language_coherence: float  # 0..1, see compute_tag_language_coherence
    grounding_ratio: float       # 0..1, see compute_grounding_ratio


def extract_tagged_sentences(text: str) -> list[tuple[str, str]]:
    """Return [(tag, sentence), ...] for every sentence carrying a claim tag."""
    results = []
    for sentence in _sentences(text):
        match = CLAIM_TAG_PATTERN.search(sentence)
        if match:
            results.append((match.group(1), sentence))
    return results


def compute_tag_language_coherence(tagged_sentences: list[tuple[str, str]]) -> float:
    """
    Proxy for internal coherence between a claim's declared type and its
    linguistic certainty markers:
      - a [FACT] sentence containing overclaim words but no hedge words is
        coherent (facts should be stated plainly); a [FACT] sentence with
        hedge words is a mild inconsistency (why hedge something you tagged
        as fact?).
      - a [SPECULATION] or [HYPOTHESIS] sentence containing overclaim words
        and no hedge words is an inconsistency (speculative claims dressed
        in certain language) -- this is the "framing drift" pattern.
      - [INFERENCE] is treated as neutral (either marker is acceptable).
    Returns the fraction of tagged sentences that are internally coherent.
    Returns 1.0 if there are no tagged sentences (nothing to be incoherent
    about) -- callers should also look at tag_coverage separately.
    """
    if not tagged_sentences:
        return 1.0

    coherent = 0
    for tag, sentence in tagged_sentences:
        hedges = _count_markers(sentence, HEDGE_MARKERS)
        overclaims = _count_markers(sentence, OVERCLAIM_MARKERS)

        if tag == "FACT":
            ok = hedges == 0
        elif tag in ("SPECULATION", "HYPOTHESIS"):
            ok = not (overclaims > 0 and hedges == 0)
        else:  # INFERENCE
            ok = True

        coherent += int(ok)

    return coherent / len(tagged_sentences)


def compute_grounding_ratio(tagged_sentences: list[tuple[str, str]], source_text: str) -> float:
    """
    Proxy for the EIG Claim-Evidence gap: what fraction of [FACT]-tagged
    sentences share at least one meaningful content word with the raw
    source article (title + abstract)? This is a crude lexical-overlap
    check, not a real entailment check -- it will miss paraphrased facts
    and can be fooled by keyword-stuffing. It mainly catches the case of a
    [FACT] claim with *zero* textual connection to the source at all.
    Returns 1.0 if there are no FACT-tagged sentences (nothing to check).
    """
    fact_sentences = [s for tag, s in tagged_sentences if tag == "FACT"]
    if not fact_sentences:
        return 1.0

    source_tokens = set(_tokenize(source_text))
    if not source_tokens:
        return 0.0

    grounded = 0
    for sentence in fact_sentences:
        sentence_tokens = set(_tokenize(sentence))
        if sentence_tokens & source_tokens:
            grounded += 1

    return grounded / len(fact_sentences)


def analyze_text(analysis_text: str, source_text: str) -> TextSignals:
    tokens = _tokenize(analysis_text)
    tagged = extract_tagged_sentences(analysis_text)
    sentences = _sentences(analysis_text)

    layers_present = {
        name for name, pattern in LAYER_PATTERNS.items()
        if pattern.search(analysis_text or "")
    }

    domain_hits = set()
    lowered = (analysis_text or "").lower()
    for cluster, keywords in DOMAIN_CLUSTERS.items():
        if any(kw in lowered for kw in keywords):
            domain_hits.add(cluster)

    return TextSignals(
        word_count=len(tokens),
        tagged_sentences=tagged,
        tag_coverage=(len(tagged) / len(sentences)) if sentences else 0.0,
        layers_present=layers_present,
        hedge_count=_count_markers(analysis_text, HEDGE_MARKERS),
        overclaim_count=_count_markers(analysis_text, OVERCLAIM_MARKERS),
        conditional_count=_count_markers(analysis_text, CONDITIONAL_MARKERS),
        implication_count=_count_markers(analysis_text, IMPLICATION_MARKERS),
        domain_hits=domain_hits,
        tag_language_coherence=compute_tag_language_coherence(tagged),
        grounding_ratio=compute_grounding_ratio(tagged, source_text),
    )


def lexical_novelty(analysis_text: str, source_text: str) -> float:
    """
    Fraction of distinct content words in the analysis that do NOT appear
    in the raw source (title + abstract). A pure restatement/summary of the
    source scores near 0; an analysis that introduces substantial new
    vocabulary (new concepts, comparisons, framing) scores higher. This is
    a proxy for "creative/generative value add", not a quality judgement --
    an analysis could score high here just by being verbose or off-topic,
    so it should be read alongside grounding_ratio, not alone.
    """
    analysis_tokens = set(_tokenize(analysis_text))
    if not analysis_tokens:
        return 0.0

    source_tokens = set(_tokenize(source_text))
    novel = analysis_tokens - source_tokens

    return len(novel) / len(analysis_tokens)
