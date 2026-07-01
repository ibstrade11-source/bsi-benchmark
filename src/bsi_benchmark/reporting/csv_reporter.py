import csv

from .base import Reporter
from .registry import registry


class CsvReporter(Reporter):

    name = "csv"

    def generate(self, result, output):
        with open(output, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Metric", "Score"])
            for k, v in result.evaluation.scores.items():
                writer.writerow([k, v])
        return output


registry.register(CsvReporter())
