"""
Tests for bsi_benchmark.stats.

Correctness of Cohen's d_z and the Wilcoxon W statistic was verified
against scipy/numpy during development (see CHANGES / commit notes) --
these tests check internal consistency and edge-case behavior, not
numerical correctness from scratch (that would just re-implement scipy
in the test file).
"""
import math

from bsi_benchmark.self_compare.models import CriterionScore, SelfComparisonRecord
from bsi_benchmark.stats import aggregate, render_markdown


def _record(pairs, title="A"):
    return SelfComparisonRecord(
        article_title=title, analyst_model="m", overall_winner="bsi",
        overall_reasoning="r",
        criteria=[CriterionScore(f"c{i}", raw, bsi) for i, (raw, bsi) in enumerate(pairs)],
    )


def test_aggregate_pools_all_criteria_across_records():
    records = [_record([(4, 8), (3, 7)]), _record([(5, 5)])]
    result = aggregate(records)
    assert result.n == 3
    assert result.n_records == 2


def test_mean_diff_sign_matches_direction():
    records = [_record([(2, 8), (3, 9)])]  # bsi consistently higher
    result = aggregate(records)
    assert result.mean_diff > 0


def test_win_tie_loss_counts():
    records = [_record([(8, 2), (2, 8), (5, 5)])]
    result = aggregate(records)
    assert result.raw_wins == 1
    assert result.bsi_wins == 1
    assert result.ties == 1


def test_cohens_dz_matches_known_value():
    # Cross-checked against numpy during development: dz ≈ 0.5410832508
    pairs = [(4, 8), (3, 7), (5, 8), (6, 7), (5, 5), (8, 5), (7, 4), (3, 9), (2, 8), (6, 6)]
    result = aggregate([_record(pairs)])
    assert result.cohens_dz is not None
    assert abs(result.cohens_dz - 0.5410832508379366) < 1e-9


def test_wilcoxon_w_matches_known_value():
    # Cross-checked against scipy.stats.wilcoxon during development: W = 6.0
    pairs = [(4, 8), (3, 7), (5, 8), (6, 7), (5, 5), (8, 5), (7, 4), (3, 9), (2, 8), (6, 6)]
    result = aggregate([_record(pairs)])
    assert result.wilcoxon_statistic == 6.0


def test_small_n_wilcoxon_flagged_in_note():
    pairs = [(4, 8), (3, 7)]  # n=2, well under the n>=10 threshold
    result = aggregate([_record(pairs)])
    assert "کوچک است" in result.wilcoxon_note


def test_single_pair_has_no_ci_or_effect_size():
    result = aggregate([_record([(4, 8)])])
    assert result.ci95_low is None
    assert result.cohens_dz is None


def test_empty_records_list_handled():
    result = aggregate([])
    assert result.n == 0
    assert result.n_records == 0
    assert math.isnan(result.mean_raw)


def test_all_zero_diffs_handled():
    result = aggregate([_record([(5, 5), (7, 7)])])
    assert result.wilcoxon_statistic is None
    assert "صفر" in result.wilcoxon_note


def test_caveats_always_present():
    result = aggregate([_record([(4, 8), (3, 7)])])
    assert len(result.caveats) >= 2


def test_markdown_contains_key_numbers():
    result = aggregate([_record([(4, 8), (3, 7)])])
    md = render_markdown(result)
    assert "میانگین" in md
    assert "نکات احتیاطی" in md
