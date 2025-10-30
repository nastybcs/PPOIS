
import unittest
from datetime import datetime
from staff.warehouse_director import WarehouseDirector
from staff.warehouse_manager import WarehouseManager
from storage.warehouse_module import Warehouse
from exceptions.errors import (
    WarehouseError, EmployeeAlreadyAppointed, TerminateError
)


class TestWarehouseDirector(unittest.TestCase):

    def setUp(self):
        self.warehouse = Warehouse("Главный склад")

        self.director = WarehouseDirector(
            "Виктор", "Петров", "Москва, Ленина, 1", "victor@warehouse.ru", self.warehouse
        )

    def test_init(self):
        self.assertEqual(self.director.first_name, "Виктор")
        self.assertEqual(self.director.last_name, "Петров")
        self.assertEqual(self.director.address, "Москва, Ленина, 1")
        self.assertEqual(self.director.email, "victor@warehouse.ru")
        self.assertEqual(self.director.warehouse.name, "Главный склад")
        self.assertTrue(self.director.is_active)
        self.assertEqual(self.director.managers, [])

    def test_full_name(self):
        self.assertEqual(self.director.full_name(), "Виктор Петров")

    def test_appoint_manager_success(self):
    
        manager = WarehouseManager("Олег", "Иванов", "СПб", "oleg@wh.ru", self.warehouse)
        
        result = self.director.appoint_manager(manager)
        
        self.assertIn(manager, self.director.managers)
        self.assertEqual(manager.director, self.director)
        self.assertIn("уже назначен", result)  

    def test_appoint_manager_different_warehouse(self):
      
        other_warehouse = Warehouse("Филиал")
        manager = WarehouseManager("Анна", "Сидорова", "Екб", None, other_warehouse)
        
        with self.assertRaises(WarehouseError) as cm:
            self.director.appoint_manager(manager)
        self.assertIn("одном складе", str(cm.exception))

    def test_appoint_manager_already_apppointed(self):
        manager = WarehouseManager("Олег", "Иванов", "СПб", None, self.warehouse)
        self.director.appoint_manager(manager)
        
        with self.assertRaises(EmployeeAlreadyAppointed) as cm:
            self.director.appoint_manager(manager)
        self.assertIn("уже назначен", str(cm.exception))

    def test_terminate_success(self):
        self.assertTrue(self.director.is_active)
        self.director.terminate()
        self.assertFalse(self.director.is_active)
        self.assertIsInstance(self.director.termination_date, datetime)

    def test_terminate_already_terminated(self):

        self.director.terminate()
        with self.assertRaises(TerminateError) as cm:
            self.director.terminate()
        self.assertIn("уже уволен", str(cm.exception))

    def test_info_dict(self):
        info = self.director.info()
        self.assertIsInstance(info, dict)
        self.assertEqual(info["name"], "Виктор Петров")
        self.assertIn("id", info)
        self.assertTrue(info["active"])
        self.assertIn("hire_date", info)
        self.assertEqual(info["warehouse"], "Главный склад")

    def test_employee_id_unique(self):
        director2 = WarehouseDirector("Мария", "Козлова", "Казань", None, self.warehouse)
        self.assertNotEqual(self.director.employee_id, director2.employee_id)
        self.assertEqual(director2.employee_id, self.director.employee_id + 1)

    def test_managers_list_after_appoint(self):
        m1 = WarehouseManager("Алексей", "Смирнов", "Москва", None, self.warehouse)
        m2 = WarehouseManager("Елена", "Васильева", "СПб", None, self.warehouse)
        
        self.director.appoint_manager(m1)
        self.director.appoint_manager(m2)
        
        self.assertEqual(len(self.director.managers), 2)
        self.assertEqual(self.director.managers[0], m1)
        self.assertEqual(self.director.managers[1], m2)

    def test_manager_director_link_after_terminate_director(self):
    
        manager = WarehouseManager("Олег", "Иванов", "СПб", None, self.warehouse)
        self.director.appoint_manager(manager)
        
        self.assertEqual(manager.director, self.director)
        
        self.director.terminate()
        
        self.assertEqual(manager.director, self.director)
        self.assertFalse(self.director.is_active)
