"""
Statistical aggregation across multiple SelfComparisonRecord files.

Deliberately dependency-free (no scipy/numpy): this tool is meant to run
on Termux/Android, where compiling scipy's Fortran/C extensions is often
impractical. Every statistic here is implemented in pure Python. This
trades some numerical polish for something that actually installs and
runs where this tool is actually used.

What this computes, over the paired (raw_score, bsi_score) observations
pooled from every criterion in every input record:

- n, mean raw, mean bsi, mean paired difference
- 95% CI on the mean difference via bootstrap resampling (percentile
  method) -- chosen over a normal-theory CI because n is typically small
  and the difference distribution is not assumed normal
- Cohen's d_z (paired-samples effect size: mean_diff / std_diff)
- Wilcoxon signed-rank test (normal approximation for the p-value) --
  a distribution-free test appropriate for paired ordinal/interval data
  that may not be normal
- win/tie/loss counts (same derivation rule as CriterionScore.winner)

Caveats stated explicitly in the output, not hidden in a docstring:
- Wilcoxon's normal approximation is a large-sample approximation;
  for n < ~10 the reported p-value is unreliable and this is flagged.
- Pooling all criteria from all records into one sample treats each
  criterion-observation as independent. It is not -- criteria within
  one record share an article and an analyst. This inflates apparent N
  and is a real limitation, not swept under the rug (see
  ROADMAP.md item on this).
"""
from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from .self_compare.models import SelfComparisonRecord


@dataclass
class AggregateStats:
    n: int
    mean_raw: float
    mean_bsi: float
    mean_diff: float
    ci95_low: Optional[float]
    ci95_high: Optional[float]
    cohens_dz: Optional[float]
    wilcoxon_statistic: Optional[float]
    wilcoxon_p_approx: Optional[float]
    wilcoxon_note: str
    raw_wins: int
    bsi_wins: int
    ties: int
    n_records: int
    caveats: List[str] = field(default_factory=list)


def _pooled_pairs(records: List[SelfComparisonRecord]) -> List[Tuple[float, float]]:
    pairs = []
    for r in records:
        for c in r.criteria:
            pairs.append((c.raw_score, c.bsi_score))
    return pairs


def _mean(xs: List[float]) -> float:
    return sum(xs) / len(xs) if xs else float("nan")


def _std(xs: List[float]) -> float:
    if len(xs) < 2:
        return float("nan")
    m = _mean(xs)
    var = sum((x - m) ** 2 for x in xs) / (len(xs) - 1)
    return math.sqrt(var)


def _bootstrap_ci(diffs: List[float], n_resamples: int = 2000, seed: int = 42) -> Tuple[Optional[float], Optional[float]]:
    if len(diffs) < 2:
        return None, None
    rng = random.Random(seed)
    n = len(diffs)
    means = []
    for _ in range(n_resamples):
        sample = [diffs[rng.randrange(n)] for _ in range(n)]
        means.append(_mean(sample))
    means.sort()
    lo_idx = int(0.025 * n_resamples)
    hi_idx = int(0.975 * n_resamples) - 1
    hi_idx = min(hi_idx, n_resamples - 1)
    return means[lo_idx], means[hi_idx]


def _wilcoxon_signed_rank(diffs: List[float]) -> Tuple[Optional[float], Optional[float], str]:
    """
    Wilcoxon signed-rank test, normal approximation, zero-differences
    dropped (standard handling). Returns (W statistic, approx p-value,
    a note about reliability at this sample size).
    """
    nonzero = [d for d in diffs if d != 0]
    n = len(nonzero)
    if n < 1:
        return None, None, "همهٔ تفاضل‌ها صفر بودند؛ آزمون قابل‌محاسبه نیست."

    abs_diffs = sorted(range(n), key=lambda i: abs(nonzero[i]))
    ranks = [0.0] * n
    i = 0
    sorted_abs = sorted(abs(d) for d in nonzero)
    # assign average rank for ties
    rank_pos = 1
    idx = 0
    while idx < n:
        j = idx
        while j < n and sorted_abs[j] == sorted_abs[idx]:
            j += 1
        avg_rank = (rank_pos + (rank_pos + (j - idx) - 1)) / 2
        for k in range(idx, j):
            ranks[k] = avg_rank
        rank_pos += (j - idx)
        idx = j

    order = sorted(range(n), key=lambda i: abs(nonzero[i]))
    signed_ranks = [0.0] * n
    for rank_i, orig_i in enumerate(order):
        signed_ranks[orig_i] = ranks[rank_i] if nonzero[orig_i] > 0 else -ranks[rank_i]

    w_plus = sum(r for r in signed_ranks if r > 0)
    w_minus = -sum(r for r in signed_ranks if r < 0)
    w = min(w_plus, w_minus)

    mean_w = n * (n + 1) / 4
    std_w = math.sqrt(n * (n + 1) * (2 * n + 1) / 24)
    if std_w == 0:
        return w, None, "انحراف‌معیار صفر شد؛ p-value قابل‌محاسبه نیست."

    z = (w - mean_w) / std_w
    # two-sided p-value from standard normal, via erf (no scipy needed)
    p = 2 * (1 - 0.5 * (1 + math.erf(abs(z) / math.sqrt(2))))
    p = max(0.0, min(1.0, p))

    note = ""
    if n < 10:
        note = (
            f"⚠️ n={n} برای تقریب نرمال Wilcoxon کوچک است (معمولاً n≥10 توصیه "
            "می‌شود) -- این p-value را با احتیاط زیاد بخوانید، نه به‌عنوان "
            "معیار قطعی."
        )
    return w, p, note


def aggregate(records: List[SelfComparisonRecord]) -> AggregateStats:
    pairs = _pooled_pairs(records)
    n = len(pairs)
    raw_scores = [p[0] for p in pairs]
    bsi_scores = [p[1] for p in pairs]
    diffs = [b - r for r, b in pairs]

    mean_raw = _mean(raw_scores)
    mean_bsi = _mean(bsi_scores)
    mean_diff = _mean(diffs)

    ci_low, ci_high = _bootstrap_ci(diffs) if n >= 2 else (None, None)

    std_diff = _std(diffs)
    cohens_dz = (mean_diff / std_diff) if (n >= 2 and std_diff and not math.isnan(std_diff) and std_diff != 0) else None

    w_stat, w_p, w_note = _wilcoxon_signed_rank(diffs) if n >= 1 else (None, None, "بدون داده")

    raw_wins = sum(1 for r, b in pairs if r > b)
    bsi_wins = sum(1 for r, b in pairs if b > r)
    ties = sum(1 for r, b in pairs if r == b)

    caveats = [
        "این آمار همهٔ معیارها از همهٔ رکوردها را در یک نمونهٔ واحد ادغام "
        "می‌کند -- معیارهای داخل یک رکورد مستقل از هم نیستند (همان مقاله، "
        "همان تحلیلگر). این N ظاهری را بزرگ‌تر از تعداد واقعی مشاهدات "
        "مستقل نشان می‌دهد.",
        "این آمار صرفاً روی داده‌های self-compare (خودگزارش‌دهی تحلیلگر) "
        "است، نه یک ارزیابی مستقل/کور. طبق طراحی توافق‌شدهٔ پروژه، این "
        "ابزار معیار تحمیل نمی‌کند -- آمار فقط توصیفیِ همان قضاوت‌های "
        "خودگزارش‌شده است.",
    ]
    if n < 10:
        caveats.append(f"n={n} کوچک است؛ هر نتیجه‌گیری قطعی از این آمار زودهنگام است.")

    return AggregateStats(
        n=n, mean_raw=mean_raw, mean_bsi=mean_bsi, mean_diff=mean_diff,
        ci95_low=ci_low, ci95_high=ci_high, cohens_dz=cohens_dz,
        wilcoxon_statistic=w_stat, wilcoxon_p_approx=w_p, wilcoxon_note=w_note,
        raw_wins=raw_wins, bsi_wins=bsi_wins, ties=ties,
        n_records=len(records), caveats=caveats,
    )


def render_markdown(stats: AggregateStats) -> str:
    lines = ["# تجمیع آماری خودمقایسه‌ها (self-compare aggregate)", ""]
    lines.append(f"**تعداد رکورد:** {stats.n_records} | **تعداد جفت‌مشاهدهٔ معیار:** {stats.n}")
    lines.append("")
    lines.append(f"- میانگین raw: {stats.mean_raw:.3f}")
    lines.append(f"- میانگین bsi: {stats.mean_bsi:.3f}")
    lines.append(f"- میانگین تفاضل (bsi - raw): {stats.mean_diff:.3f}")
    if stats.ci95_low is not None:
        lines.append(f"- فاصلهٔ اطمینان ۹۵٪ (bootstrap) برای تفاضل: [{stats.ci95_low:.3f}, {stats.ci95_high:.3f}]")
    else:
        lines.append("- فاصلهٔ اطمینان: قابل‌محاسبه نبود (n کمتر از ۲)")
    if stats.cohens_dz is not None:
        lines.append(f"- Cohen's d_z (اندازهٔ اثر جفت‌شده): {stats.cohens_dz:.3f}")
    else:
        lines.append("- Cohen's d_z: قابل‌محاسبه نبود")
    if stats.wilcoxon_p_approx is not None:
        lines.append(f"- Wilcoxon signed-rank: W={stats.wilcoxon_statistic:.1f}, p≈{stats.wilcoxon_p_approx:.4f} (تقریب نرمال)")
    else:
        lines.append("- Wilcoxon signed-rank: قابل‌محاسبه نبود")
    if stats.wilcoxon_note:
        lines.append(f"  {stats.wilcoxon_note}")
    lines.append("")
    lines.append(f"**برد/باخت در سطح معیار:** raw برنده {stats.raw_wins}، bsi برنده {stats.bsi_wins}، مساوی {stats.ties}")
    lines.append("")
    lines.append("## نکات احتیاطی (حذف‌نشدنی)")
    for c in stats.caveats:
        lines.append(f"- {c}")
    lines.append("")
    return "\n".join(lines)
