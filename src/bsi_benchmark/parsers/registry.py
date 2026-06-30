class ParserRegistry:

    def __init__(self):
        self._parsers = {}

    def register(self, provider, parser):
        self._parsers[provider] = parser

    def get(self, provider):
        return self._parsers[provider]

    def available(self):
        return sorted(self._parsers.keys())


registry = ParserRegistry()
