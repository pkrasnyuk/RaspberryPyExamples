from abc import ABC, abstractmethod


class BaseDataProcessing(ABC):
    @abstractmethod
    def processing(self) -> None:
        pass
