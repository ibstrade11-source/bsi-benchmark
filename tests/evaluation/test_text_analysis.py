"""Unit tests for the text_analysis proxy utilities themselves."""
from bsi_benchmark.evaluation.text_analysis import (
    extract_tagged_sentences,
    compute_tag_language_coherence,
    compute_grounding_ratio,
    lexical_novelty,
    analyze_text,
)


def test_extract_tagged_sentences_finds_all_four_tag_types():
    text = (
        "[FACT] A is true. [INFERENCE] B follows from A. "
        "[HYPOTHESIS] C might explain B. [SPECULATION] D is a wild guess."
    )
    tagged = extract_tagged_sentences(text)
    tags_found = {tag for tag, _ in tagged}
    assert tags_found == {"FACT", "INFERENCE", "HYPOTHESIS", "SPECULATION"}


def test_grounding_ratio_zero_for_unrelated_fact_claim():
    source = "This paper is about coffee prices in Brazil."
    tagged = [("FACT", "[FACT] The moon is made of cheese.")]
    ratio = compute_grounding_ratio(tagged, source)
    assert ratio == 0.0


def test_grounding_ratio_one_for_overlapping_fact_claim():
    source = "This paper studies coffee prices in Brazil during droughts."
    tagged = [("FACT", "[FACT] Coffee prices in Brazil rose during the drought.")]
    ratio = compute_grounding_ratio(tagged, source)
    assert ratio == 1.0


def test_lexical_novelty_zero_for_verbatim_restatement():
    source = "Coffee prices rose sharply during the drought season."
    analysis = "Coffee prices rose sharply during the drought season."
    assert lexical_novelty(analysis, source) == 0.0


def test_lexical_novelty_high_for_disjoint_vocabulary():
    source = "Coffee prices rose sharply during the drought season."
    analysis = "Quantum entanglement violates local realism in Bell test experiments."
    assert lexical_novelty(analysis, source) == 1.0


def test_analyze_text_detects_meta_layer_in_persian():
    text = "لایه Meta (فرا): این تحلیل معنای عمیق‌تری دارد."
    signals = analyze_text(text, source_text="")
    assert "meta" in signals.layers_present


def test_analyze_text_tag_coverage_reflects_fraction_of_tagged_sentences():
    text = "[FACT] First sentence. Second untagged sentence. Third untagged sentence."
    signals = analyze_text(text, source_text="")
    assert 0.0 < signals.tag_coverage < 1.0
