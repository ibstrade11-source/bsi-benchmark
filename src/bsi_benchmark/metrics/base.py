from abc import ABC
from abc import abstractmethod


class Metric(ABC):

    name: str

    @abstractmethod
    def evaluate(self, dataset):
        raise NotImplementedError
