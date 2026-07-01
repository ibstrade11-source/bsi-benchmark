from .registry import registry


class ReportManager:

    def generate(self, reporter, result):
        return registry.get(reporter).generate(result)
