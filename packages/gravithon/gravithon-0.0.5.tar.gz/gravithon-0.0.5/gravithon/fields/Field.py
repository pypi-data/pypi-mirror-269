from abc import ABC, abstractmethod
from numpy import array, ndarray


class Field(ABC):
    value: ndarray

    # TODO: field boundaries

    def __str__(self):
        return f'  Value: {self.value} '  # units are field dependent

    def dimensions(self):
        return len(self.value)
