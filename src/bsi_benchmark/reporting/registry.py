class ReporterRegistry:

    def __init__(self):
        self._reporters = {}

    def register(self, reporter):
        self._reporters[reporter.name] = reporter

    def get(self, name):
        return self._reporters[name]


registry = ReporterRegistry()
