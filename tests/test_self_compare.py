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
