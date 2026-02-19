from abc import ABC, abstractmethod
from objects.IShootable import IShootable


class Weapon(IShootable, ABC):
    def __init__(self, ammo: int, caliber: int):
        self._ammo = ammo
        self._caliber = caliber
        self._is_loaded = True

    @property
    def ammo(self) -> int:
        return self._ammo

    @property
    def is_loaded(self) -> bool:
        return self._is_loaded

    @property
    def is_empty(self) -> bool:
        return self._ammo <= 0
    
    @abstractmethod
    def fire(self) -> None:
        pass

    def reload(self) -> None:
        self._is_loaded = True
        print("Weapon is reloaded")

    def to_dict(self) -> dict[str, any]:
        return {
            "ammo": self._ammo,
            "caliber": self._caliber,
            "is_loaded": self._is_loaded,
        }

    def from_dict(self, data: dict[str, any]) -> None:
        self._ammo = data.get("ammo", self._ammo)
        self._caliber = data.get("caliber", self._caliber)
        self._is_loaded = data.get("is_loaded", self._is_loaded)
