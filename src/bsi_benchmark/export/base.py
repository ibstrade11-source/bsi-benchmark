from abc import ABC, abstractmethod


class Exporter(ABC):

    @abstractmethod
    def export(self, result, path):
        raise NotImplementedError
