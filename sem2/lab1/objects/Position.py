import math


class Position:
    def __init__(self, x: int = 0, y: int = 0):
        self.__x = x
        self.__y = y

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    @property
    def coordinates(self) -> tuple[int, int]:
        return (self.__x, self.__y)

    def distance_to(self, other: "Position") -> float:

        dx = self.__x - other.__x
        dy = self.__y - other.__y
        return math.sqrt(dx * dx + dy * dy)

    def to_dict(self) -> dict[str, int]:
        return {"x": self.__x, "y": self.__y}

    def from_dict(self, data: dict[str, int]) -> None:
        self.__x = data.get("x", self.__x)
        self.__y = data.get("y", self.__y)
    def __str__(self):
        return f"({self.x}, {self.y})"
