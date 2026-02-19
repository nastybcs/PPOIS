import unittest
import os
from unittest.mock import patch
from objects.Tank import Tank



class TestTankCoverage(unittest.TestCase):
    
    def setUp(self):
        self.tank = Tank(load_from_file=False)
        self.tank.add_member("Тестовый")
        self.tank.add_member("Тестовый2")
        self.tank.add_member("Тестовый3")
        self.tank.board_crew()
        if os.path.exists("tank_save.json"):
            os.remove("tank_save.json")
    
    def tearDown(self):
        if os.path.exists("tank_save.json"):
            os.remove("tank_save.json")
    
    def test_is_combat_ready_all_true(self):
        self.tank.start_engine()
        self.tank._Tank__cannon._ammo = 10
        self.assertTrue(self.tank.is_combat_ready)
    
    def test_is_combat_ready_crew_not_ready(self):
        self.tank.start_engine()
        self.tank._Tank__crew._Crew__is_ready = False
        self.assertFalse(self.tank.is_combat_ready)
    
    def test_is_combat_ready_engine_not_running(self):
        self.tank._Tank__cannon._ammo = 10
        self.assertFalse(self.tank.is_combat_ready)
    
    def test_is_combat_ready_no_fuel(self):
        self.tank.start_engine()
        self.tank._Tank__fuel_tank._FuelTank__level = 0
        self.tank._Tank__cannon._ammo = 10
        self.assertFalse(self.tank.is_combat_ready)
    
    def test_is_combat_ready_no_ammo(self):
        self.tank.start_engine()
        self.tank._Tank__cannon._ammo = 0
        self.assertFalse(self.tank.is_combat_ready)
    
    def test_move_to_engine_not_running(self):
        self.tank.stop_engine()
        result = self.tank.move_to(100, 100)
        self.assertFalse(result)
    
    def test_move_to_crew_not_ready(self):
        self.tank.start_engine()
        self.tank._Tank__crew._Crew__is_ready = False
        result = self.tank.move_to(100, 100)
        self.assertFalse(result)
    
    def test_move_to_not_enough_fuel(self):
        self.tank.start_engine()
        self.tank._Tank__fuel_tank._FuelTank__level = 10
        result = self.tank.move_to(100, 0)  
        self.assertFalse(result)
    
    def test_move_to_success(self):
        self.tank.start_engine()
        old_x = self.tank.position.x
        result = self.tank.move_to(50, 0)
        self.assertTrue(result)
        self.assertNotEqual(self.tank.position.x, old_x)
    
    def test_shoot_cannon_engine_not_running(self):
        self.tank.stop_engine()
        initial_ammo = self.tank.ammo
        result = self.tank.shoot_cannon()
        self.assertFalse(result)
        self.assertEqual(self.tank.ammo, initial_ammo)
    
    def test_start_engine_no_fuel(self):
        self.tank._Tank__fuel_tank._FuelTank__level = 0
        result = self.tank.start_engine()
        self.assertFalse(result)
        self.assertFalse(self.tank.engine_is_running())
    
    def test_start_engine_success(self):
        result = self.tank.start_engine()
        self.assertTrue(result)
        self.assertTrue(self.tank.engine_is_running())
    
    def test_refuel_with_amount(self):
        self.tank._Tank__fuel_tank._FuelTank__level = 100
        self.tank.refuel(200)
        self.assertEqual(self.tank.fuel_level, 300)
    
    def test_get_crew_info_empty(self):
        empty_tank = Tank(load_from_file=False)
        info = empty_tank.get_crew_info()
        self.assertIn("Crew is empty", info)
    
    def test_get_crew_info_with_members(self):
        info = self.tank.get_crew_info()
        self.assertIn("Crew (3 people)", info)
        self.assertIn("Тестовый", info)
        self.assertIn("Тестовый2", info)
        self.assertIn("Тестовый3", info)
    
    def test_from_dict_missing_keys(self):
        data = {}
        self.tank.from_dict(data) 
        self.assertTrue(True)
    
    @patch("builtins.open", side_effect=Exception("Test error"))
    def test_save_state_error(self, mock_open):
        result = self.tank.save_state()
        self.assertFalse(result)
    
    def test_delete_save_file_not_exists(self):
        if os.path.exists("tank_save.json"):
            os.remove("tank_save.json")
        result = self.tank.delete_save()
        self.assertFalse(result)
    
    def test_crew_is_ready_property(self):
        self.assertTrue(self.tank.crew_is_ready)
        self.tank._Tank__crew._Crew__is_ready = False
        self.assertFalse(self.tank.crew_is_ready)
    
    def test_has_fuel_property(self):
        self.assertTrue(self.tank.has_fuel)
        self.tank._Tank__fuel_tank._FuelTank__level = 0
        self.assertFalse(self.tank.has_fuel)
    
    def test_can_move_property(self):
        self.tank.start_engine()
        self.assertTrue(self.tank.can_move)
        self.tank._Tank__crew._Crew__is_ready = False
        self.assertFalse(self.tank.can_move)
    
    def test_move_method(self):
        self.tank.start_engine()
        old_x = self.tank.position.x
        result = self.tank.move(50)
        self.assertTrue(result)
        self.assertEqual(self.tank.position.x, old_x + 50)
    
    def test_engine_is_running(self):
        self.assertFalse(self.tank.engine_is_running())
        self.tank.start_engine()
        self.assertTrue(self.tank.engine_is_running())
    
    def test_stop_engine(self):
        self.tank.start_engine()
        self.assertTrue(self.tank.engine_is_running())
        self.tank.stop_engine()
        self.assertFalse(self.tank.engine_is_running())
    
    def test_show_crew(self):
        with patch("builtins.print") as mock_print:
            self.tank.show_crew()
            mock_print.assert_called_once()
    
    def test_board_crew(self):
        self.tank._Tank__crew._Crew__is_ready = False
        result = self.tank.board_crew()
        self.assertTrue(result)
        self.assertTrue(self.tank._Tank__crew.is_ready)
    
    def test_leave_crew(self):
        self.tank._Tank__crew._Crew__is_ready = True
        result = self.tank.leave_crew()
        self.assertFalse(result)
        self.assertFalse(self.tank._Tank__crew.is_ready)
    
    def test_add_member(self):
        initial_count = len(self.tank._Tank__crew._Crew__members)
        self.tank.add_member("Новый")
        new_count = len(self.tank._Tank__crew._Crew__members)
        self.assertEqual(new_count, initial_count + 1)
    
    def test_remove_crew_member(self):
        self.tank.add_member("ДляУдаления")
        initial_count = len(self.tank._Tank__crew._Crew__members)
        self.tank.remove_crew_member("ДляУдаления")
        new_count = len(self.tank._Tank__crew._Crew__members)
        self.assertEqual(new_count, initial_count - 1)
    
    def test_to_dict(self):
        data = self.tank.to_dict()
        self.assertIn("position", data)
        self.assertIn("fuel_tank", data)
        self.assertIn("engine", data)
        self.assertIn("cannon", data)
        self.assertIn("crew", data)
    
    def test_load_state_file_not_found(self):
        if os.path.exists("tank_save.json"):
            os.remove("tank_save.json")
        result = self.tank.load_state()
        self.assertFalse(result)
    
    def test_load_state_success(self):
        self.tank.save_state()
        new_tank = Tank(load_from_file=False)
        result = new_tank.load_state()
        self.assertTrue(result)
    
    def test_load_state_error(self):
        with open("tank_save.json", "w") as f:
            f.write("invalid json")
        
        result = self.tank.load_state()
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()