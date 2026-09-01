import json
from .base import Reporter
from .registry import registry


class JsonReporter(Reporter):
    name = "json"

    def generate(self, result):
        return json.dumps(
            {
                "provider": result.provider,
                "query": result.query,
                "articles": len(result.articles),
            },
            indent=2,
            ensure_ascii=False,
        )


registry.register(JsonReporter())
