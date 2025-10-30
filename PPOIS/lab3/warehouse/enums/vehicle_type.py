from enum import Enum

class VehicleType(Enum):
    TRUCK = ("грузовик", 10_000)
    VAN = ("фургон", 1_500)
    CAR = ("легковой", 300)
    MOTORCYCLE = ("мотоцикл", 50)

    def __init__(self, name_ru, default_capacity_kg):
        self.name_ru = name_ru
        self.default_capacity_kg = default_capacity_kg

    def capacity(self):
        return self.default_capacity_kg