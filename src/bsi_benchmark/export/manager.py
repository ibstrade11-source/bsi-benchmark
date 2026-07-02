from .registry import registry


class ExportManager:

    def export(self, result, fmt, path):
        exporter = registry.get(fmt)
        return exporter.export(result, path)
