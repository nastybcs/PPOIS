import unittest
from storage.warehouse_module import Warehouse
from core.product import Product
from storage.location import Location 
from utils.warehouse_checker import WarehouseChecker  

class TestWarehouseChecker(unittest.TestCase):

    def setUp(self):
    
        self.warehouse = Warehouse("Склад №1")
        self.product1 = Product("Молоко", "P001", 80, 1.0)
        self.product2 = Product("Телевизор", "P002", 30000, 10.0)
        self.warehouse.register_product(self.product1)
        self.warehouse.register_product(self.product2)
        self.loc1 = Location("Холодильник")
        self.loc2 = Location("Зал хранения")

        self.warehouse.add_location(self.loc1)
        self.warehouse.add_location(self.loc2)
        self.checker = WarehouseChecker(self.warehouse)

    def test_quick_check_counts(self):
      
        result = self.checker.quick_check()
        self.assertEqual(result, "Склад: 2 товаров, 2 локаций")

    def test_quick_check_empty_warehouse(self):
      
        empty_wh = Warehouse("Пустой склад")
        checker = WarehouseChecker(empty_wh)
        result = checker.quick_check()
        self.assertEqual(result, "Склад: 0 товаров, 0 локаций")

    def test_quick_check_dynamic_update(self):
       
        new_product = Product("Хлеб", "P003", 40, 0.5)
        self.warehouse.register_product(new_product)

        result = self.checker.quick_check()
        self.assertEqual(result, "Склад: 3 товаров, 2 локаций")

    def test_quick_check_after_new_location(self):

        new_loc = Location("Дополнительный отсек")
        self.warehouse.add_location(new_loc)

        result = self.checker.quick_check()
        self.assertEqual(result, "Склад: 2 товаров, 3 локаций")

