import json

from .base import Reporter
from .registry import registry


class JsonReporter(Reporter):

    name = "json"

    def generate(self, result):
        return json.dumps(
            {
                "evaluator": result.evaluator,
                "scores": result.scores,
            },
            indent=2,
        )


registry.register(JsonReporter())
