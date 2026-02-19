from abc import ABC, abstractmethod


class IShootable(ABC):
    @abstractmethod
    def fire(self) -> None:
        pass

    @abstractmethod
    def reload(self) -> None:
        pass
