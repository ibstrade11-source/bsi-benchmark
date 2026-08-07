import csv
from .base import Reporter
from .registry import registry


class CsvReporter(Reporter):
    name = "csv"

    def generate(self, result, output):
        with open(output, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            writer.writerow(["Metric", "Score"])
            writer.writerow(["BSI", "N/A"])

        return output


registry.register(CsvReporter())
