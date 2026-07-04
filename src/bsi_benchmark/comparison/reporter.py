"""
Plain-text/markdown rendering of a ComparisonReport, for CLI output and for
copy-pasting into a writeup. Kept dependency-free (no pandas/tabulate) to
match the rest of the project's minimal-dependency style.
"""

from .result import ComparisonReport

DIM_ORDER = ["D1", "D2", "D3", "D4", "D5", "D6", "D7", "BSI", "grounding_ratio", "tag_coverage"]


def render_markdown(report: ComparisonReport) -> str:
    lines = [f"# Comparison: {report.dataset_name}", ""]

    if report.run_metadata:
        m = report.run_metadata
        commit = m.get("git_commit") or "unknown (not a git checkout, or git unavailable)"
        dirty = m.get("git_dirty")
        dirty_note = " (uncommitted local changes present)" if dirty else ""
        lines.append("## Run metadata")
        lines.append(f"- bsi-benchmark version: {m.get('tool_version')}")
        lines.append(f"- git commit: {commit}{dirty_note}")
        lines.append(f"- run timestamp (UTC): {m.get('run_timestamp_utc')}")
        lines.append(f"- methodology note: {m.get('methodology_note')}")
        lines.append("")

    if report.source_url:
        lines.append(
            f"> BSI prompt source (read it yourself, unedited): {report.source_url}"
        )
        lines.append("")

    for result in report.results:
        title = result.article.title or "(untitled)"
        lines.append(f"## {title}")
        if result.article.url or result.article.doi:
            prov = []
            if result.article.url:
                prov.append(f"source: {result.article.url}")
            if result.article.doi:
                prov.append(f"doi: {result.article.doi}")
            lines.append(f"*{' | '.join(prov)}*")
        lines.append("")
        header = "| generator | mode | " + " | ".join(DIM_ORDER) + " |"
        sep = "|---|---|" + "|".join(["---"] * len(DIM_ORDER)) + "|"
        lines.append(header)
        lines.append(sep)

        for cell in result.cells:
            if cell.failed:
                row = f"| {cell.generator} | {cell.mode} | ERROR: {cell.scores['error']} |"
                lines.append(row)
                continue

            values = " | ".join(f"{cell.scores.get(d, 0.0):.3f}" for d in DIM_ORDER)
            lines.append(f"| {cell.generator} | {cell.mode} | {values} |")

        lines.append("")

    return "\n".join(lines)
