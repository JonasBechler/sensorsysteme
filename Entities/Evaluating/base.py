from abc import ABC, abstractmethod


class IEvaluationStrategy(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def dataPoints(self):
        pass

    @abstractmethod
    def evaluate(self, img, positions, times):
        pass

    def __str__(self):
        return self.name