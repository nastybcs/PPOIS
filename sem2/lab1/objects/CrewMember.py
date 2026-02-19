class CrewMember:
    def __init__(self, name: str):
        self.__name = name

    @property
    def name(self):
        return self.__name


    def to_dict(self) -> dict[str, any]:

        return {
            "name": self.__name
        }


    def __str__(self) -> str:
        return f"{self.__name})"
