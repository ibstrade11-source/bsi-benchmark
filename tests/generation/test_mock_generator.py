from bsi_benchmark.generation import MockGenerator
from bsi_benchmark.models import Article

ARTICLE = Article(title="Sample Title", abstract="Sample abstract content.")


def test_mock_generator_raw_mode_returns_plain_text():
    gen = MockGenerator()
    analysis = gen.generate(ARTICLE, "Analyze plainly.\n\nTitle: {title}\nAbstract: {abstract}")
    assert "Sample Title" in analysis.text
    assert analysis.source_model == "mock"


def test_mock_generator_bsi_mode_includes_layers_and_tags():
    gen = MockGenerator()
    analysis = gen.generate(ARTICLE, "Follow the BSI master prompt.\n\nTitle: {title}\nAbstract: {abstract}")
    assert "[FACT]" in analysis.text
    assert "لایه" in analysis.text
