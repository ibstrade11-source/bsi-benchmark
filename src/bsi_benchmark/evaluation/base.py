from abc import ABC, abstractmethod


class Evaluator(ABC):

    name: str

    @abstractmethod
    def evaluate(self, dataset):
        raise NotImplementedError
