from .base import Parser
from .registry import registry
from bsi_benchmark.models.article import Article


class MockParser(Parser):
    """
    Parses MockProvider's raw output (a plain list[dict], not a JSON
    string like the real providers return) into Article objects. Exists so
    `--provider mock` is actually usable end-to-end for offline testing --
    previously MockProvider was registered but had no parser wired into
    PipelineRunner.parsers, so it always raised KeyError.
    """

    def parse(self, raw):
        return [
            Article(title=entry.get("title", ""), abstract=entry.get("abstract", ""))
            for entry in raw
        ]


registry.register("mock", MockParser())
