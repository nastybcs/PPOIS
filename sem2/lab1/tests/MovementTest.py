import unittest
import sys
from objects.Tank import Tank


class TestMovement(unittest.TestCase):

    def setUp(self):
        print("\n" + "=" * 60)
        print("СОЗДАНИЕ НОВОГО ТАНКА")
        print("=" * 60)
        self.tank = Tank(load_from_file=False)
        print("✅ Танк создан")
        sys.stdout.flush()

    def print_state(self, stage):
        print(f"\n--- {stage} ---")
        print(f"Позиция: {self.tank.position}")
        print(f"Двигатель работает: {self.tank.engine_is_running()}")
        print(f"Экипаж готов: {self.tank.crew_is_ready}")
        print(f"Топливо: {self.tank.fuel_level}л")
        print(f"can_move: {self.tank.can_move}")
        sys.stdout.flush()

    def test_move_with_debug(self):
        self.tank.add_member("Водитель")
        self.tank.add_member("Наводчик")
        self.tank.add_member("Заряжающий")
        self.tank.board_crew()
        engine_result = self.tank.start_engine()
        print(f"\n🔧 Запуск двигателя: {engine_result}")
        print(f"   is_running: {self.tank.engine_is_running()}")
        print(f"\n🚀 can_move: {self.tank.can_move}")
        print("\n🎯 Попытка движения...")
        old_x = self.tank.position.x
        result = self.tank.move_to(50, 20)
        print("\n📊 Результат движения:")
        print(f"   move_to вернул: {result}")
        print(f"   Было: x={old_x}")
        print(f"   Стало: x={self.tank.position.x}")
        self.assertTrue(result, "move_to вернул False!")
        self.assertNotEqual(self.tank.position.x, old_x, "Позиция не изменилась!")

    def test_crew_boarding(self):
        print("\nПРОВЕРКА ПОСАДКИ ЭКИПАЖА")
        self.tank.add_member("Водитель")
        self.tank.add_member("Наводчик")
        self.tank.add_member("Заряжающий")

        print(f"Экипаж до посадки: {self.tank.crew_is_ready}")
        self.tank.board_crew()

        print(f"Экипаж после посадки: {self.tank.crew_is_ready}")
        self.assertTrue(self.tank.crew_is_ready, "Экипаж не готов после посадки!")

    def test_engine_start(self):
        print("\nПРОВЕРКА ЗАПУСКА ДВИГАТЕЛЯ")

        print(f"До запуска: {self.tank.engine_is_running()}")

        result = self.tank.start_engine()

        print(f"После запуска: {self.tank.engine_is_running()}")
        print(f"Результат: {result}")

        self.assertTrue(self.tank.engine_is_running(), "Двигатель не запустился!")


if __name__ == "__main__":
    unittest.main()
