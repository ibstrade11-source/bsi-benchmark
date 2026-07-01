import json

from .model import BenchmarkConfig


class ConfigLoader:

    def load(self, path):

        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        return BenchmarkConfig(**data)
