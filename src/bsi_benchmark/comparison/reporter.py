"""
Plain-text/markdown rendering of a ComparisonReport, for CLI output and for
copy-pasting into a writeup. Kept dependency-free (no pandas/tabulate) to
match the rest of the project's minimal-dependency style.
"""

from .result import ComparisonReport

DIM_ORDER = ["D1", "D2", "D3", "D4", "D5", "D6", "D7", "BSI", "grounding_ratio", "tag_coverage"]


def render_markdown(report: ComparisonReport) -> str:
    lines = [f"# Comparison: {report.dataset_name}", ""]

    for result in report.results:
        title = result.article.title or "(untitled)"
        lines.append(f"## {title}")
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
