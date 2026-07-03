from pathlib import Path


class HtmlReport:

    def generate(self, result, output):
        output = Path(output)
        output.parent.mkdir(parents=True, exist_ok=True)

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

<h2>Overall</h2>

<p>BSI Score: {result.evaluation.scores.get("BSI", "Not Available")}</p>

</body>
</html>
"""

        output.write_text(html, encoding="utf-8")
        return output
