class LLMRegistry:

    def __init__(self):
        self._models = {}

    def register(self, name, backend):
        self._models[name] = backend

    def get(self, name):
        return self._models[name]

    def names(self):
        return sorted(self._models.keys())
