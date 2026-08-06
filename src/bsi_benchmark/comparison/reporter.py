"""
Minimal Markdown reporter.

Comparison reports are based on the independent LLM Judge.
No internal BSI evaluator scores are rendered.
"""

from .result import ComparisonReport


def render_markdown(report: ComparisonReport) -> str:
    lines = [f"# Comparison: {report.dataset_name}", ""]

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

        if result.article.url:
            lines.append(f"*source:* {result.article.url}")

        if result.article.doi:
            lines.append(f"*doi:* {result.article.doi}")

        lines.append("")

        jr = None

        for cell in result.cells:
            if cell.judge_result:
                jr = cell.judge_result
                break

        if jr is None:
            lines.append("No judge result.")
            lines.append("")
            continue

        lines.append("### Judge Evaluation")
        lines.append("")

        if "winner" in jr:
            lines.append(f"- **Winner:** {jr['winner']}")

        if "reasoning" in jr:
            lines.append(f"- **Reasoning:** {jr['reasoning']}")

        criteria = jr.get("criteria")

        if isinstance(criteria, list):

            lines.append("")
            lines.append("#### Independent Judge Criteria")
            lines.append("")
            lines.append("| Criterion | Importance | Raw | BSI | Reason |")
            lines.append("|---|---:|---:|---:|---|")

            for item in criteria:

                lines.append(
                    f"| {item.get('name','')} "
                    f"| {item.get('importance','')} "
                    f"| {item.get('raw_score','')} "
                    f"| {item.get('bsi_score','')} "
                    f"| {item.get('reason','')} |"
                )

        totals = jr.get("total_scores")

        if isinstance(totals, dict):

            lines.append("")
            lines.append("#### Judge Total Scores")
            lines.append("")
            lines.append("| Raw | BSI |")
            lines.append("|---:|---:|")
            lines.append(
                f"| {totals.get('raw','')} | {totals.get('bsi','')} |"
            )

        lines.append("")


        if cell.judge_result:
            jr = cell.judge_result

            lines.append("")
            lines.append("### Judge Result")
            lines.append("")
            lines.append(f"- Winner: {jr.get('winner','')}")
            lines.append(f"- Reasoning: {jr.get('reasoning','')}")

            totals = jr.get("total_scores")
            if isinstance(totals, dict):
                lines.append("")
                lines.append("| Raw | BSI |")
                lines.append("|---:|---:|")
                lines.append(
                    f"| {totals.get('raw','')} | {totals.get('bsi','')} |"
                )

    return "\n".join(lines)
