class Engine:
    def __init__(self, horsepower: int = 120):
        self.__horsepower = horsepower
        self.__is_running = False

    def start(self) -> bool:
        self.__is_running = True
        print("Engine was started")
        return True

    def stop(self) -> bool:
        self.__is_running = False
        return False

    @property
    def horsepower(self) -> int:
        return self.__horsepower

    @property
    def is_running(self) -> bool:
        return self.__is_running

    def to_dict(self) -> dict[str, any]:
        return {"horsepower": self.__horsepower, "is_running": self.__is_running}

    def from_dict(self, data: dict[str, any]) -> None:

        self.__horsepower = data.get("horsepower", self.__horsepower)
        self.__is_running = data.get("is_running", False)
