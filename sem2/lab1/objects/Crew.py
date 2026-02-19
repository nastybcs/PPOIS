from objects.CrewMember import CrewMember
from exceptions.CrewMemberNotFoundError import CrewMemberNotFoundError


class Crew:
    def __init__(self):
        self.__members: list[CrewMember] = []
        self.__is_ready: bool = False

    @property
    def is_ready(self) -> bool:
        return self.__is_ready

    def board(self) -> bool:
        self.__is_ready = True
        print("Crew is in tank")
        return True

    def leave(self) -> None:
        self.__is_ready = False
        print("Crew is out of tank")

    def add_member(self, name: str) -> None:
        new_member = CrewMember(name)
        self.__members.append(new_member)
        print(f"{new_member.name} was added")

    def remove_member(self, name: str) -> None:
        for i, member in enumerate(self.__members):
            if member.name == name:
                removed = self.__members.pop(i)
                print(f"Was removed: {removed}")
                return
        raise CrewMemberNotFoundError(f"{name} was not found")

    def __str__(self) -> str:
        if not self.__members:
            return "Crew: empty"

        status = " ready" if self.__is_ready else "not ready"
        result = f" Crew ({len(self.__members)} people, {status}):\n"
        for m in self.__members:
            result += f"    {m}\n"
        return result

    def to_dict(self) -> dict[str, any]:
        return {
            "members": [m.to_dict() for m in self.__members],
            "is_ready": self.__is_ready,
        }
    def from_dict(self, data: dict[str, any]) -> None:
        self.__members = []
        for member_data in data.get("members", []):
            member = CrewMember(
                member_data.get("name", ""),
            )
            self.__members.append(member)
        self.__is_ready = data.get("is_ready", False)

