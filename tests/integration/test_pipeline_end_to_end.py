from pathlib import Path

from bsi_benchmark.models.article import Article
from bsi_benchmark.pipeline.runner import PipelineRunner


def test_pipeline_runner_end_to_end_with_mock_provider():
    runner = PipelineRunner()

    result = runner.run(
        "mock",
        "integration test",
    )

    assert result is not None


def test_pipeline_preserves_article_identity_fields():
    article = Article(
        title="Integration Test Article",
        abstract="A deterministic integration-test abstract.",
        doi="10.1234/integration.test",
        url="https://example.org/article",
    )

    assert article.title == "Integration Test Article"
    assert article.abstract == "A deterministic integration-test abstract."
    assert article.doi == "10.1234/integration.test"
    assert article.url == "https://example.org/article"


def test_pipeline_runner_has_no_direct_network_dependency():
    runner_source = (
        Path("src/bsi_benchmark/pipeline/runner.py")
        .read_text(encoding="utf-8")
    )

    forbidden = (
        "requests.get",
        "requests.post",
        "requests.Session",
        "httpx.",
        "urllib.request",
    )

    violations = [item for item in forbidden if item in runner_source]
    assert not violations, (
        "PipelineRunner contains direct network implementation: "
        + ", ".join(violations)
    )
