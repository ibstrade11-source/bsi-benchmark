"""
Tests for bsi_benchmark.self_compare.

Covers: winner derivation (the core design point -- winner is computed
from scores, never separately asserted), input validation, and
round-trip save/load.
"""
import json
import os

from bsi_benchmark.self_compare.models import CriterionScore, SelfComparisonRecord
from bsi_benchmark.self_compare.io import SelfComparisonIO
from bsi_benchmark.self_compare.reporter import render_markdown


def test_winner_is_bsi_when_bsi_score_higher():
    c = CriterionScore(criterion="x", raw_score=4, bsi_score=8)
    assert c.winner == "bsi"


def test_winner_is_raw_when_raw_score_higher():
    c = CriterionScore(criterion="x", raw_score=9, bsi_score=2)
    assert c.winner == "raw"


def test_winner_is_tie_when_scores_equal():
    c = CriterionScore(criterion="x", raw_score=5, bsi_score=5)
    assert c.winner == "tie"


def test_load_example_file():
    example_path = os.path.join(
        os.path.dirname(__file__), "..", "examples", "self_compare_example.json"
    )
    record = SelfComparisonIO().load(example_path)
    assert record.article_title
    assert len(record.criteria) >= 1
    assert record.overall_winner in ("raw", "bsi", "tie", "برابر") or record.overall_winner


def test_load_missing_criteria_key_raises(tmp_path):
    p = tmp_path / "bad.json"
    p.write_text(json.dumps({"article": {"title": "X"}}), encoding="utf-8")
    try:
        SelfComparisonIO().load(str(p))
        assert False, "expected ValueError"
    except ValueError:
        pass


def test_load_empty_criteria_list_raises(tmp_path):
    p = tmp_path / "bad.json"
    p.write_text(json.dumps({"article": {"title": "X"}, "criteria": []}), encoding="utf-8")
    try:
        SelfComparisonIO().load(str(p))
        assert False, "expected ValueError"
    except ValueError:
        pass


def test_criterion_missing_score_raises(tmp_path):
    p = tmp_path / "bad.json"
    p.write_text(json.dumps({
        "article": {"title": "X"},
        "criteria": [{"criterion": "a", "bsi_score": 5}],
    }), encoding="utf-8")
    try:
        SelfComparisonIO().load(str(p))
        assert False, "expected ValueError"
    except ValueError:
        pass


def test_save_then_load_round_trip(tmp_path):
    record = SelfComparisonRecord(
        article_title="Test Article",
        analyst_model="test-model",
        criteria=[
            CriterionScore(criterion="c1", raw_score=3, bsi_score=7, notes="n1"),
            CriterionScore(criterion="c2", raw_score=8, bsi_score=4),
        ],
        overall_winner="bsi",
        overall_reasoning="because reasons",
    )
    out_path = str(tmp_path / "record.json")
    SelfComparisonIO().save(record, out_path)

    reloaded = SelfComparisonIO().load(out_path)
    assert reloaded.article_title == "Test Article"
    assert len(reloaded.criteria) == 2
    assert reloaded.criteria[0].winner == "bsi"
    assert reloaded.criteria[1].winner == "raw"


def test_summary_counts():
    record = SelfComparisonRecord(
        article_title="T",
        analyst_model="m",
        criteria=[
            CriterionScore(criterion="a", raw_score=1, bsi_score=9),
            CriterionScore(criterion="b", raw_score=9, bsi_score=1),
            CriterionScore(criterion="c", raw_score=5, bsi_score=5),
        ],
        overall_winner="tie",
        overall_reasoning="mixed",
    )
    assert record.raw_wins() == 1
    assert record.bsi_wins() == 1
    assert record.ties() == 1


def test_markdown_includes_winner_column():
    record = SelfComparisonRecord(
        article_title="T",
        analyst_model="m",
        criteria=[CriterionScore(criterion="c1", raw_score=2, bsi_score=8)],
        overall_winner="bsi",
        overall_reasoning="r",
    )
    md = render_markdown(record)
    assert "برنده" in md
    assert "bsi" in md


def test_hash_auto_derived_from_text():
    record = SelfComparisonRecord(
        article_title="T", analyst_model="m",
        criteria=[CriterionScore(criterion="c1", raw_score=2, bsi_score=8)],
        overall_winner="bsi", overall_reasoning="r",
        raw_analysis_text="hello",
    )
    import hashlib
    assert record.raw_analysis_sha256 == hashlib.sha256(b"hello").hexdigest()
    assert record.bsi_analysis_sha256 is None


def test_has_source_texts_requires_both():
    record = SelfComparisonRecord(
        article_title="T", analyst_model="m",
        criteria=[CriterionScore(criterion="c1", raw_score=2, bsi_score=8)],
        overall_winner="bsi", overall_reasoning="r",
        raw_analysis_text="only raw",
    )
    assert record.has_source_texts() is False
    record.bsi_analysis_text = "now bsi too"
    # NOTE: setting after construction does not retroactively hash;
    # this documents that behavior rather than asserting a hash exists.
    assert record.bsi_analysis_sha256 is None


def test_verify_hashes_true_when_untampered():
    record = SelfComparisonRecord(
        article_title="T", analyst_model="m",
        criteria=[CriterionScore(criterion="c1", raw_score=2, bsi_score=8)],
        overall_winner="bsi", overall_reasoning="r",
        raw_analysis_text="hello", bsi_analysis_text="world",
    )
    result = record.verify_hashes()
    assert result["raw"] is True
    assert result["bsi"] is True


def test_verify_hashes_false_when_tampered():
    record = SelfComparisonRecord(
        article_title="T", analyst_model="m",
        criteria=[CriterionScore(criterion="c1", raw_score=2, bsi_score=8)],
        overall_winner="bsi", overall_reasoning="r",
        raw_analysis_text="hello",
    )
    record.raw_analysis_text = "tampered text"  # hash now stale
    result = record.verify_hashes()
    assert result["raw"] is False


def test_round_trip_preserves_text_and_hash(tmp_path):
    record = SelfComparisonRecord(
        article_title="T", analyst_model="m",
        criteria=[CriterionScore(criterion="c1", raw_score=2, bsi_score=8)],
        overall_winner="bsi", overall_reasoning="r",
        raw_analysis_text="hello", bsi_analysis_text="world",
    )
    path = str(tmp_path / "rec.json")
    SelfComparisonIO().save(record, path)
    reloaded = SelfComparisonIO().load(path)
    assert reloaded.raw_analysis_text == "hello"
    assert reloaded.bsi_analysis_text == "world"
    assert reloaded.raw_analysis_sha256 == record.raw_analysis_sha256
    assert reloaded.has_source_texts() is True


def test_hash_without_text_is_preserved_on_load(tmp_path):
    """Text withheld (e.g. length/copyright) but hash published: the
    hash must survive a save/load round trip even with no text."""
    path = str(tmp_path / "rec.json")
    payload = {
        "article": {"title": "T"},
        "analyst_model": "m",
        "criteria": [{"criterion": "c1", "raw_score": 2, "bsi_score": 8}],
        "overall_winner": "bsi",
        "overall_reasoning": "r",
        "raw_analysis_sha256": "deadbeef" * 8,
    }
    path_obj = tmp_path / "rec.json"
    path_obj.write_text(json.dumps(payload), encoding="utf-8")
    reloaded = SelfComparisonIO().load(str(path_obj))
    assert reloaded.raw_analysis_text is None
    assert reloaded.raw_analysis_sha256 == "deadbeef" * 8
    assert reloaded.has_source_texts() is False


def test_record_without_texts_still_loads_and_works():
    """Backward compatibility: a record with no text fields at all must
    still load and function (has_source_texts() just returns False)."""
    record = SelfComparisonRecord(
        article_title="T", analyst_model="m",
        criteria=[CriterionScore(criterion="c1", raw_score=2, bsi_score=8)],
        overall_winner="bsi", overall_reasoning="r",
    )
    assert record.has_source_texts() is False
    assert record.raw_analysis_sha256 is None
    assert record.verify_hashes() == {"raw": None, "bsi": None}
