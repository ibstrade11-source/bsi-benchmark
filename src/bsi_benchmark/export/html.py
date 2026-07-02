from pathlib import Path
from .registry import registry


class HtmlReport:

    def export(self, result, path):

        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>BSI Benchmark Report</title>
</head>
<body>

<h1>BSI Benchmark Report</h1>

<p><b>Provider:</b> {result.dataset.provider}</p>
<p><b>Query:</b> {result.dataset.query}</p>

<h2>Scores</h2>

<ul>
{''.join(f'<li>{k}: {v}</li>' for k, v in result.evaluation.scores.items())}
</ul>

</body>
</html>
"""

        path.write_text(html, encoding="utf-8")
        return path


registry.register("html", HtmlReport())
