"""Deterministic cross-provider pipeline validation.

This test must not depend on live provider APIs, quotas, DNS,
or external rate limits. Live provider behavior belongs to
integration/benchmark runs, not the deterministic pytest suite.
"""

import json

from bsi_benchmark.pipeline import PipelineRunner


def test_cross_provider(monkeypatch):
    crossref_response = {
        "message": {
            "items": [
                {
                    "DOI": "10.0000/test-crossref",
                    "title": ["Artificial Intelligence"],
                    "abstract": "Offline validation article.",
                    "URL": "https://doi.org/10.0000/test-crossref",
                }
            ]
        }
    }

    arxiv_response = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <id>http://arxiv.org/abs/test</id>
    <title>Artificial Intelligence</title>
    <summary>Offline validation article.</summary>
  </entry>
</feed>
"""

    class FakeResponse:
        def __init__(self, body):
            self.ok = True
            self.status_code = 200
            self.body = body

    def fake_get(self, url, *args, **kwargs):
        if "api.crossref.org" in url:
            return FakeResponse(json.dumps(crossref_response))
        if "export.arxiv.org" in url:
            return FakeResponse(arxiv_response)
        raise AssertionError(f"Unexpected external URL in deterministic test: {url}")

    monkeypatch.setattr(
        "bsi_benchmark.network.HttpClient.get",
        fake_get,
    )

    runner = PipelineRunner()

    for provider in ("crossref", "arxiv"):
        result = runner.run(provider, "Artificial Intelligence")
        assert result is not None
        assert result.provider == provider
        assert len(result.articles) > 0
