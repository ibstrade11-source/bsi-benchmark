"""
Markdown rendering for a SelfComparisonRecord -- the analyst's own
comparison table, WITH the derived Winner column per criterion.
"""
from __future__ import annotations

from .models import SelfComparisonRecord

_WINNER_LABEL = {"raw": "raw", "bsi": "bsi", "tie": "مساوی"}


def render_markdown(record: SelfComparisonRecord) -> str:
    lines = [f"# خودمقایسهٔ تحلیلگر — {record.article_title}", ""]

    if record.article_doi or record.article_url:
        prov = []
        if record.article_url:
            prov.append(f"source: {record.article_url}")
        if record.article_doi:
            prov.append(f"doi: {record.article_doi}")
        lines.append(f"*{' | '.join(prov)}*")
        lines.append("")

    lines.append(f"**تحلیلگر:** {record.analyst_model}")
    lines.append("")

    if record.criteria_rationale:
        lines.append("## معیارهای انتخابی تحلیلگر (به زبان خودش)")
        lines.append(record.criteria_rationale)
        lines.append("")

    lines.append("## جدول مقایسه")
    lines.append("| معیار | raw | bsi | برنده | یادداشت |")
    lines.append("|---|---|---|---|---|")
    for c in record.criteria:
        note = c.notes or ""
        lines.append(
            f"| {c.criterion} | {c.raw_score:g} | {c.bsi_score:g} "
            f"| {_WINNER_LABEL[c.winner]} | {note} |"
        )
    lines.append("")

    lines.append(
        f"**جمع‌بندی معیارها:** raw برنده در {record.raw_wins()} مورد، "
        f"bsi برنده در {record.bsi_wins()} مورد، "
        f"مساوی در {record.ties()} مورد."
    )
    lines.append("")

    lines.append("## نتیجهٔ نهایی تحلیلگر")
    lines.append(f"**ترجیح کلی:** {record.overall_winner}")
    lines.append("")
    lines.append(record.overall_reasoning)
    lines.append("")

    if record.run_metadata:
        m = record.run_metadata
        lines.append("## متادیتای اجرا")
        lines.append(f"- bsi-benchmark version: {m.get('tool_version')}")
        lines.append(f"- git commit: {m.get('git_commit') or 'unknown'}")
        lines.append(f"- run timestamp (UTC): {m.get('run_timestamp_utc')}")
        lines.append("")

    return "\n".join(lines)
