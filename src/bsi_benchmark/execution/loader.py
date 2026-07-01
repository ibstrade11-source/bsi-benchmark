from bsi_benchmark.datasets import DatasetIO


class DatasetLoader:

    def __init__(self):
        self.io = DatasetIO()

    def load(self, filename):
        return self.io.load(filename)
