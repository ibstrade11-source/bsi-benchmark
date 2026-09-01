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

<p><b>Provider:</b> {result.provider}</p>
<p><b>Query:</b> {result.query}</p>

<h2>Scores</h2>

<ul>
<li>BSI: N/A</li>
</ul>

<h2>Articles</h2>

<p>Total Articles: {len(result.articles)}</p>

</body>
</html>
"""

        output.write_text(html, encoding="utf-8")
        return output
