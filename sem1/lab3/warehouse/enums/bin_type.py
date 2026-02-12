from enum import Enum
class BinType(Enum):
    STANDARD = "Стандартная"
    FRIDGE = "Холодильная"
    CHEMICAL = "Химическая"
    HAZARD = "Опасная"
    SEALED_BOX = "Запечатанная коробка"
    STACKED_PALLET = "Паллета в штабеле"
    SMALL_BOX = "Маленькая коробка"
    LARGE_PALLET = "Большая паллета"