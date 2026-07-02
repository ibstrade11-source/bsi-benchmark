class ExportRegistry:

    def __init__(self):
        self._exporters = {}

    def register(self, name: str, exporter):
        self._exporters[name] = exporter

    def get(self, name: str):
        return self._exporters[name]


registry = ExportRegistry()
