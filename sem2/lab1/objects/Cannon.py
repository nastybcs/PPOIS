from objects.Weapon import Weapon


class Cannon(Weapon):
    def __init__(self, ammo: int = 30, caliber: int = 125):
        super().__init__(ammo, caliber)

    def fire(self) -> None:
        if not self._is_loaded:
            print("Cannon is unloaded")
            return

        if self.is_empty:
            print("Cannon is empty")
            return
        self._ammo -= 1
        self._is_loaded = False
        print(f"{self._caliber}mm cannon fired")
        print(f" There are {self._ammo} ammo left")
