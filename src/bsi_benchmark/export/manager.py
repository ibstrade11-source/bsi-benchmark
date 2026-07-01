from .json_exporter import JsonExporter
from bsi_benchmark.reporting.html import HtmlReport
from bsi_benchmark.reporting.csv_reporter import CsvReporter


class ExportManager:

    def export(self, result, fmt, path):

        fmt = fmt.lower()

        if fmt == "json":
            return JsonExporter().export(result, path)

        if fmt == "html":
            return HtmlReport().generate(result, path)

        if fmt == "csv":
            return CsvReporter().generate(result, path)

        raise ValueError(f"Unsupported export format: {fmt}")
