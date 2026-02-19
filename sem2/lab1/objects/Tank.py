from objects.Position import Position
from objects.FuelTank import FuelTank
from objects.Engine import Engine
from objects.Cannon import Cannon
from objects.Crew import Crew
import json
import os
import copy

class Tank:
    FUEL_CONSUMPTION_RATE = 2.0
    SAVE_FILE = "tank_save.json"

    def __init__(self, start_x: int = 0, start_y: int = 0, load_from_file: bool = True):
        self.__position = Position(start_x, start_y)
        self.__fuel_tank = FuelTank(400)
        self.__fuel_consumption_rate = self.FUEL_CONSUMPTION_RATE
        self.__engine = Engine()
        self.__cannon = Cannon()
        self.__crew = Crew()

        if load_from_file:
            self.load_state()

    @property
    def fuel_level(self) -> int:
        return self.__fuel_tank.level

    @property
    def crew_is_ready(self) -> bool:
        return self.__crew.is_ready

    @property
    def fuel_percentage(self) -> float:
        return self.__fuel_tank.percentage

    @property
    def has_fuel(self) -> bool:
        return not self.__fuel_tank.is_empty

    @property
    def is_combat_ready(self) -> bool:
        return (
            self.__crew.is_ready
            and self.__engine.is_running
            and self.has_fuel
            and self.__cannon.ammo > 0
        )

    @property
    def ammo(self) -> int:
        return self.__cannon.ammo

    @property
    def position(self) -> Position:
        return self.__position

    @property
    def can_move(self) -> bool:
        return self.__engine.is_running and self.__crew.is_ready and self.has_fuel

    def move_to(self, target_x: float, target_y: float) -> bool:
        print(f"\nMoving to ({target_x}, {target_y})")

        if not self.__engine.is_running:
            print("Engine is not running")
            return False

        if not self.__crew.is_ready:
            print("Crew is not ready")
            return False

        target = Position(target_x, target_y)
        distance = self.__position.distance_to(target)
        fuel_needed = distance * self.__fuel_consumption_rate

        print(f"Distance: {distance:.1f} km")
        print(f"Fuel need: {fuel_needed}l")

        if fuel_needed > self.__fuel_tank.level:
            print(f"Not enough fuel! There are {self.__fuel_tank.level}l")
            return False

        if not self.__fuel_tank.consume(fuel_needed):
            return False

        self.__position = target
        print(f"Tank reached the destination {self.__position.x} {self.__position.y}")
        return True

    def move(self, distance: int) -> bool:
        return self.move_to(self.__position.x + distance, self.__position.y)

    def shoot_cannon(self) -> bool:
        if not self.__engine.is_running:
            print("Engine is not running")
            return False
        return self.__cannon.fire()

    def engine_is_running(self) -> bool:
        return self.__engine.is_running

    def start_engine(self) -> bool:
        if self.__fuel_tank.is_empty:
            print("There is no fuel")
            return False
        return self.__engine.start()

    def stop_engine(self) -> bool:
        return self.__engine.stop()

    def refuel(self, amount: int = None) -> None:
        self.__fuel_tank.refill(amount)

    def add_member(self, name: str) -> None:
        self.__crew.add_member(name)

    def remove_crew_member(self, name: str) -> None:
        self.__crew.remove_member(name)

    def show_crew(self)->None:
        print(self.__crew)

    def board_crew(self) -> bool:
        self.__crew.board()
        return True

    def leave_crew(self) -> bool:
        self.__crew.leave()
        return False

    def get_crew_info(self) -> str:

        members = self.__crew._Crew__members
        if not members:
            return "Crew is empty"

        info = f"Crew ({len(members)} people):\n"
        for m in members:
            info += f"  - {m}\n"
        return info

    def to_dict(self) -> dict[str, any]:
        return {
            "position": self.__position.to_dict(),
            "fuel_tank": self.__fuel_tank.to_dict(),
            "engine": self.__engine.to_dict(),
            "cannon": self.__cannon.to_dict(),
            "crew": self.__crew.to_dict(),
        }

    def from_dict(self, data: dict[str, any]) -> None:
        if "position" in data:
            self.__position.from_dict(data["position"])
        if "fuel_tank" in data:
            self.__fuel_tank.from_dict(data["fuel_tank"])
        if "engine" in data:
            self.__engine.from_dict(data["engine"])
        if "cannon" in data:
            self.__cannon.from_dict(data["cannon"])
        if "crew" in data:
            self.__crew.from_dict(data["crew"])

        print("Loaded")

    def save_state(self, filename: str = None) -> bool:
        if filename is None:
            filename = self.SAVE_FILE

        try:
            data = self.to_dict()
            data_copy = copy.deepcopy(data)
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data_copy, f, indent=2, ensure_ascii=False)
            print(f"Saved in {filename}")
            return True
        except Exception as e:
            print(f" Saving Error: {e}")
            return False


    def load_state(self, filename: str = None) -> bool:
        if filename is None:
            filename = self.SAVE_FILE

        if not os.path.exists(filename):
            print(f" {filename} not found")
            return False

        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.from_dict(data)
            print(f"loaded from {filename}")
            return True
        except Exception as e:
            print(f"Loading Error: {e}")
            return False

    def delete_save(self, filename: str = None) -> bool:
        if filename is None:
            filename = self.SAVE_FILE

        if os.path.exists(filename):
            os.remove(filename)
            print(f"File {filename} was deleted")
            return True
        return False

    def get_status(self) -> None:
        print("\n" + "=" * 50)
        print("           Status")
        print("=" * 50)
        print(f" Position: {self.__position.x} {self.__position.y}")
        print(f"Fuel: {self.__fuel_tank.level}л ({self.fuel_percentage:.1f}%)")
        print(f"Cannon: {self.__cannon.ammo} ammos")
        print(f"Engine: {'running' if self.__engine.is_running else 'stop'}")
        print(f"Crew: {'in ' if self.__crew.is_ready else 'out'}")
        print("=" * 50)
