from types import SimpleNamespace

from bsi_benchmark.comparison.runner import CrossModelRunner


class FakeArticle:
    title = "Test Article"
    abstract = "Test abstract"


class FakeDataset:
    def __init__(self):
        self.articles = [FakeArticle()]


class FakeGenerator:
    def generate(self, article, template):
        prompt = template.format(
            title=article.title,
            abstract=article.abstract,
        )
        return SimpleNamespace(
            text=f"analysis for {prompt}",
            source_model="fake-model",
            generated_at=None,
        )


def test_generator_initialization_failure_is_recorded(monkeypatch):
    runner = CrossModelRunner()

    spec = SimpleNamespace(
        generators=["broken-generator"],
        prompt_modes={"raw": "RAW {title} {abstract}"},
        judge=None,
    )

    monkeypatch.setattr(
        runner.generator_manager,
        "create",
        lambda name: (_ for _ in ()).throw(RuntimeError("generator boom")),
    )

    result = runner.run(FakeDataset(), spec)

    cell = result.results[0].cells[0]

    assert cell.generator == "broken-generator"
    assert cell.mode == "error"
    assert cell.failed is True
    assert cell.analysis is None
    assert cell.judge_result is None
    assert cell.scores == {}
    assert (
        "generator initialization failed: generator boom"
        in cell.metadata["error"]
    )


def test_judge_initialization_failure_does_not_stop_generation(monkeypatch):
    runner = CrossModelRunner()

    spec = SimpleNamespace(
        generators=["test-generator"],
        prompt_modes={
            "raw": "RAW {title} {abstract}",
            "bsi": "BSI {title} {abstract}",
        },
        judge=None,
    )

    monkeypatch.setattr(
        runner.generator_manager,
        "create",
        lambda name: FakeGenerator(),
    )

    monkeypatch.setattr(
        runner,
        "_build_judge",
        lambda *args, **kwargs: (
            _ for _ in ()
        ).throw(RuntimeError("judge boom")),
    )

    result = runner.run(FakeDataset(), spec)

    cells = result.results[0].cells

    assert len(cells) == 2
    assert {cell.mode for cell in cells} == {"raw", "bsi"}

    for cell in cells:
        assert cell.failed is False
        assert cell.analysis is not None
        assert cell.judge_result is not None
        assert (
            "judge initialization failed: judge boom"
            in cell.judge_result["error"]
        )
