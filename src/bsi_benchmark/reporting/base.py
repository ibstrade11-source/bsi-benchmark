from abc import ABC, abstractmethod


class Reporter(ABC):

    name: str

    @abstractmethod
    def generate(self, result):
        raise NotImplementedError
