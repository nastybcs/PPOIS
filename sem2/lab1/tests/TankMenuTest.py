import unittest
from unittest.mock import patch
import sys
from io import StringIO
import os
import json
import time

from objects.Tank import Tank
from menu.TankMenu import TankMenu
from objects.CrewMember import CrewMember


class TestTankMenuReal(unittest.TestCase):

    def setUp(self):
        self.tank = Tank(load_from_file=False)
        self.menu = TankMenu()
        self.menu.tank = self.tank
        self.tank.add_member(CrewMember("Тестовый"))
        self.tank.add_member(CrewMember("Тестовый2"))
        self.tank.add_member(CrewMember("Тестовый3"))
        self.tank.board_crew()
        self.held_output = StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.held_output
        if os.path.exists("tank_save.json"):
            os.remove("tank_save.json")

    def tearDown(self):
        sys.stdout = self.original_stdout
        if os.path.exists("tank_save.json"):
            os.remove("tank_save.json")

    def get_output(self):
        return self.held_output.getvalue()

    def test_show_status(self):
        with patch("builtins.input", return_value=""):
            self.menu.show_status()

        output = self.get_output()
        self.assertIn("STATUS", output.upper())
        self.assertIn("Position", output)
        self.assertIn("Fuel", output)

    def test_start_engine_success(self):
        self.tank.stop_engine()

        with patch("builtins.input", return_value=""):
            self.menu.start_engine()

        self.assertTrue(self.tank._Tank__engine.is_running)
        output = self.get_output()
        self.assertIn("engine is running", output.lower())

    def test_start_engine_already_running(self):
        self.tank.start_engine()

        with patch("builtins.input", return_value=""):
            self.menu.start_engine()

        output = self.get_output()
        self.assertIn("engine is running", output.lower())

    def test_start_engine_no_fuel(self):
        self.tank.stop_engine()
        while not self.tank._Tank__fuel_tank.is_empty:
            self.tank._Tank__fuel_tank.consume(100)

        with patch("builtins.input", return_value=""):
            self.menu.start_engine()

        self.assertFalse(self.tank._Tank__engine.is_running)
        output = self.get_output()
        self.assertIn("there is no fuel", output.lower())

    def test_stop_engine(self):
        self.tank.start_engine()

        with patch("builtins.input", return_value=""):
            self.menu.stop_engine()

        self.assertFalse(self.tank._Tank__engine.is_running)

    def test_move_to_valid_coordinates(self):
        self.tank.add_member("Водитель")
        self.tank.add_member("Наводчик")
        self.tank.add_member("Заряжающий")
        self.tank.start_engine()
        self.tank.board_crew()
        print(f"\n📍 Начальная позиция: {self.tank.position}")
        old_x = self.tank.position.x
        old_y = self.tank.position.y
        result = self.tank.move_to(50, 20)
        print(f"Результат move_to: {result}")
        print(f"📍 Конечная позиция: {self.tank.position}")
        print(f"   Старая: ({old_x}, {old_y})")
        print(f"   Новая: ({self.tank.position.x}, {self.tank.position.y})")
        self.assertNotEqual(self.tank.position.x, old_x, "X не изменился!")
        self.assertNotEqual(self.tank.position.y, old_y, "Y не изменился!")

    def test_move_to_invalid_coordinates(self):
        self.tank.start_engine()
        start_x = self.tank.position.x

        with patch("builtins.input", side_effect=["abc", "def", ""]):
            self.menu.move_tank()

        self.assertEqual(self.tank.position.x, start_x)  

    def test_move_without_engine(self):
        self.tank.stop_engine()
        start_x = self.tank.position.x

        with patch("builtins.input", side_effect=["100", "200", ""]):
            self.menu.move_tank()

        self.assertEqual(self.tank.position.x, start_x)  
        output = self.get_output()
        self.assertIn("engine is not running", output.lower())

    def test_move_without_fuel(self):
        self.tank.start_engine()
        while not self.tank._Tank__fuel_tank.is_empty:
            self.tank._Tank__fuel_tank.consume(100)

        start_x = self.tank.position.x

        with patch("builtins.input", side_effect=["100", "200", ""]):
            self.menu.move_tank()

        self.assertEqual(self.tank.position.x, start_x) 
        output = self.get_output()
        self.assertIn("not enough fuel", output.lower())

    def test_shoot_cannon_with_engine(self):
        self.tank.start_engine()
        initial_ammo = self.tank.ammo

        with patch("builtins.input", return_value="y"):
            self.menu.shoot_cannon()

        self.assertEqual(self.tank.ammo, initial_ammo - 1)
        output = self.get_output()
        self.assertIn("fired", output.lower())

    def test_shoot_cannon_without_engine(self):
        self.tank.stop_engine()
        initial_ammo = self.tank.ammo

        with patch("builtins.input", return_value="y"):
            self.menu.shoot_cannon()

        self.assertEqual(self.tank.ammo, initial_ammo)  
        output = self.get_output()
        self.assertIn("engine is not running", output.lower())

    def test_shoot_cannon_cancel(self):
        self.tank.start_engine()
        initial_ammo = self.tank.ammo

        with patch("builtins.input", return_value="n"):
            self.menu.shoot_cannon()

        self.assertEqual(self.tank.ammo, initial_ammo)

    def test_refuel_full(self):
        self.tank._Tank__fuel_tank.consume(100)

        with patch("builtins.input", side_effect=["1", ""]):
            self.menu.refuel_tank()

        self.assertEqual(self.tank.fuel_level, 400)  
    def test_refuel_partial(self):
        self.tank._Tank__fuel_tank.consume(200)
        level_before = self.tank.fuel_level

        with patch("builtins.input", side_effect=["2", "100", ""]):
            self.menu.refuel_tank()

        self.assertEqual(self.tank.fuel_level, level_before + 100)

    def test_refuel_invalid_amount(self):
        self.tank._Tank__fuel_tank.consume(100)
        level_before = self.tank.fuel_level

        with patch("builtins.input", side_effect=["2", "abc", ""]):
            self.menu.refuel_tank()

        self.assertEqual(self.tank.fuel_level, level_before) 

    def test_add_crew_member(self):
        initial_count = len(self.tank._Tank__crew._Crew__members)

        with patch("builtins.input", side_effect=["Новый", "1", ""]):
            self.menu.add_crew_member()

        new_count = len(self.tank._Tank__crew._Crew__members)
        self.assertEqual(new_count, initial_count + 1)

    def test_remove_crew_member_existing(self):
        self.tank.add_member("УникальныйТест")
        initial_count = len(self.tank._Tank__crew._Crew__members)

        with patch("builtins.input", side_effect=["УникальныйТест",""]):
            self.menu.remove_crew_member()

        new_count = len(self.tank._Tank__crew._Crew__members)
        self.assertEqual(new_count, initial_count - 1)


    def test_show_crew(self):
        with patch("builtins.input", return_value=""):
            self.menu.show_crew()

        output = self.get_output()
        self.assertIn("Тестовый", output) 

    def test_load_game(self):
        self.tank.save_state()
        time.sleep(0.2)
        new_tank = Tank(load_from_file=False)
        menu = TankMenu()
        menu.tank = new_tank

        with patch("builtins.input", return_value=""):
            menu.load_game()
        self.assertIsNotNone(new_tank.position)

    def test_delete_save(self):
        if os.path.exists("tank_save.json"):
            os.remove("tank_save.json")
        with open("tank_save.json", "w") as f:
            json.dump({"test": "data"}, f)
        self.assertTrue(os.path.exists("tank_save.json"), "Файл не создался!")
        with patch("builtins.input", return_value="y"):
            self.menu.delete_save()
        time.sleep(0.2)
        self.assertFalse(os.path.exists("tank_save.json"), "Файл не удалился!")

    def test_delete_save_cancel(self):
        if os.path.exists("tank_save.json"):
            os.remove("tank_save.json")
        with open("tank_save.json", "w") as f:
            json.dump({"test": "data"}, f)
        time.sleep(0.1)
        self.assertTrue(os.path.exists("tank_save.json"))
        with patch("builtins.input", return_value="n"):
            self.menu.delete_save()

        time.sleep(0.1)
        self.assertTrue(os.path.exists("tank_save.json"))
        os.remove("tank_save.json")

    def test_full_mission_sequence(self):

        self.tank.start_engine()
        self.tank._Tank__crew._Crew__is_ready = True

        start_x = self.tank.position.x

        with patch("builtins.input", side_effect=["10", "20", ""]):
            self.menu.move_tank()

        self.assertNotEqual(self.tank.position.x, start_x, "Танк не сдвинулся!")
        ammo_before = self.tank.ammo
        with patch("builtins.input", return_value="y"):
            self.menu.shoot_cannon()
        self.assertEqual(self.tank.ammo, ammo_before - 1, "Снаряд не потратился!")
    def test_print_menu(self):
        self.menu.print_menu()
        output = self.get_output()
        self.assertIn("OPTIONS:", output)
        self.assertIn("Show status", output)
        self.assertIn("Start Engine", output)
    def test_remove_crew_member_shows_crew(self):
        with patch("builtins.input", side_effect=["", ""]):
            self.menu.remove_crew_member()
        output = self.get_output()
        self.assertIn("Current crew:", output)
    def test_exit_program_with_save(self):
        with patch("builtins.input", side_effect=["y"]):
            self.menu.exit_program()
        
        self.assertFalse(self.menu.running)
        self.assertTrue(os.path.exists("tank_save.json"))
        
    def test_exit_program_without_save(self):
        with patch("builtins.input", side_effect=["n"]):
            self.menu.exit_program()
        
        self.assertFalse(self.menu.running)
        self.assertFalse(os.path.exists("tank_save.json"))

if __name__ == "__main__":
    unittest.main()
