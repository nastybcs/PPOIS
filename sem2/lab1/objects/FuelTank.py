class FuelTank:
    def __init__(self, capacity: int = 400):
        self.__capacity = capacity
        self.__level = capacity

    @property
    def level(self) -> int:
        return self.__level

    @property
    def percentage(self) -> float:
        return (self.__level / self.__capacity) * 100

    @property
    def is_empty(self) -> bool:
        return self.__level <= 0

    def refill(self, amount: int = None) -> None:
        if amount is None:
            self.__level = self.__capacity
            print(f"full refueling {self.__capacity}l")
        else:
            old = self.__level
            self.__level = min(self.__level + amount, self.__capacity)
            filled = self.__level - old
            print(f"refueled {filled}l")

    def consume(self, amount: int) -> bool:
        if amount <= 0:
            return False
        if self.__level >= amount:
            self.__level -= amount
            return True
        return False

    def to_dict(self) -> dict[str, any]:
        return {"level": self.__level, "capacity": self.__capacity}

    def from_dict(self, data: dict[str, any]) -> None:
        self.__level = data.get("level", self.__capacity)
        self.__capacity = data.get("capacity", self.__capacity)
