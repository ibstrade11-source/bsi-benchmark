from abc import ABC, abstractmethod

class Provider(ABC):

    name = "base"

    @abstractmethod
    def search(self, domain, limit):
        pass
