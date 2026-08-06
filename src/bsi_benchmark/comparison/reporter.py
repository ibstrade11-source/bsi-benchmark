"""
Markdown reporter for comparison runs.

Reports preserve judge provenance:
- criteria source
- score scale
- weights
- normalized weighted scores
- final comparison result

The judge selects criteria. Suggested criteria are only fallback metadata.
"""

from .result import ComparisonReport


def render_markdown(report: ComparisonReport) -> str:
    lines = [
        f"# Comparison: {report.dataset_name}",
        ""
    ]

    if report.run_metadata:
        m = report.run_metadata

        lines.append("## Run metadata")
        lines.append(f"- bsi-benchmark version: {m.get('tool_version')}")
        lines.append(f"- git commit: {m.get('git_commit')}")
        lines.append(f"- run timestamp (UTC): {m.get('run_timestamp_utc')}")

        if m.get("methodology_note"):
            lines.append(f"- methodology: {m.get('methodology_note')}")

        lines.append("")

    if report.source_url:
        lines.append(f"> BSI prompt source: {report.source_url}")
        lines.append("")

    for result in report.results:

        lines.append(f"## {result.article.title}")
        lines.append("")

        if result.article.url:
            lines.append(f"*source:* {result.article.url}")

        if result.article.doi:
            lines.append(f"*doi:* {result.article.doi}")

        lines.append("")

        judge = None

        for cell in result.cells:
            if cell.judge_result:
                judge = cell.judge_result
                break

        if not judge:
            lines.append("### Judge Evaluation")
            lines.append("")
            lines.append("No judge result.")
            lines.append("")
            continue

        lines.append("### Judge Evaluation")
        lines.append("")

        lines.append("#### Judge Information")
        lines.append("")
        lines.append("| Field | Value |")
        lines.append("|---|---|")
        lines.append(
            f"| Criteria source | {judge.get('criteria_source','judge')} |"
        )
        lines.append(
            f"| Score scale | {judge.get('scale','0-10')} |"
        )
        lines.append(
            f"| Weight sum | {judge.get('weight_sum','100')} |"
        )
        lines.append("")

        lines.append("#### Judge Reasoning")
        lines.append("")
        lines.append(f"**Winner:** {judge.get('winner','')}")
        lines.append("")
        lines.append(judge.get("reasoning",""))
        lines.append("")

        criteria = judge.get("criteria", [])

        lines.append("#### Criteria Selected by Judge")
        lines.append("")
        lines.append(
            "| Criterion | Weight | Raw (/10) | BSI (/10) | Weighted Raw | Weighted BSI | Explanation |"
        )
        lines.append(
            "|---|---:|---:|---:|---:|---:|---|"
        )

        raw_total = 0.0
        bsi_total = 0.0

        for item in criteria:

            weight = float(item.get("importance", 0))
            raw = float(item.get("raw_score", 0))
            bsi = float(item.get("bsi_score", 0))

            weighted_raw = round(raw * weight / 100, 2)
            weighted_bsi = round(bsi * weight / 100, 2)

            raw_total += weighted_raw
            bsi_total += weighted_bsi

            lines.append(
                f"| {item.get('name','')} "
                f"| {weight:.0f} "
                f"| {raw:.1f} "
                f"| {bsi:.1f} "
                f"| {weighted_raw:.2f} "
                f"| {weighted_bsi:.2f} "
                f"| {item.get('reason','')} |"
            )

        lines.append("")

        lines.append("#### Final Scores")
        lines.append("")
        lines.append("| Analysis | Score (/10) |")
        lines.append("|---|---:|")
        lines.append(f"| Raw | {raw_total:.2f} |")
        lines.append(f"| BSI | {bsi_total:.2f} |")

        lines.append("")

        diff = round(bsi_total - raw_total, 2)

        lines.append("#### Summary")
        lines.append("")
        lines.append(f"- Winner: **{judge.get('winner','')}**")
        lines.append(f"- Score difference: **{diff:+.2f}**")
        lines.append(
            f"- Criteria evaluated: **{len(criteria)}**"
        )

        lines.append("")

        lines.append("#### Score Formula")
        lines.append("")
        lines.append(
            "Final score = Σ(weight × criterion score / 100)"
        )
        lines.append("")


    return "\n".join(lines)
