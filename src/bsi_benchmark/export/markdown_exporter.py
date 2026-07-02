from pathlib import Path
from .registry import registry


class MarkdownExporter:

    def export(self, result, path):

        path = Path(path)

        text = f"""# BSI Benchmark Report
**Provider:** {result.dataset.provider}
**Query:** {result.dataset.query}
**Articles:** {len(result.dataset.articles)}

## Scores
"""

        for k, v in result.evaluation.scores.items():
            text += f"- **{k}**: {v}\n"

        path.write_text(text, encoding="utf-8")
        return path


registry.register("md", MarkdownExporter())
registry.register("markdown", MarkdownExporter())
