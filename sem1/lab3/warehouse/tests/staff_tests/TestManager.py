
import unittest
from staff.warehouse_manager import WarehouseManager
from staff.storekeeper import Storekeeper
from staff.loader import Loader
from core.product import Product
from storage.warehouse_module import Warehouse
from storage.location import Location
from storage.bin import Bin
from storage.batch import Batch
from orders.order import Order
from enums.product_category import Category
from enums.uom import UOM
from enums.order_status import OrderStatus
from enums.bin_type import BinType
from exceptions.errors import (
    WarehouseError, EmployeeAlreadyAppointed, OrderAlreadyExist,
   
)


class TestWarehouseManager(unittest.TestCase):

    def setUp(self):

        self.warehouse = Warehouse("Склад Москва")
        self.manager = WarehouseManager(
            "Алексей", "Смирнов", "Москва, ул. Победы, 10", "alex@wh.ru", self.warehouse
        )

    def test_init(self):
        self.assertEqual(self.manager.first_name, "Алексей")
        self.assertEqual(self.manager.last_name, "Смирнов")
        self.assertEqual(self.manager.warehouse.name, "Склад Москва")
        self.assertIsNone(self.manager.director)
        self.assertEqual(self.manager.storekeepers, [])
        self.assertEqual(self.manager.loaders, [])
        self.assertEqual(self.manager.managed_orders, [])

    def test_appoint_storekeeper_success(self):
        storekeeper = Storekeeper("Иван", "Петров", "Москва", "ivan@wh.ru", self.warehouse)
        result = self.manager.appoint_storekeeper(storekeeper)
        
        self.assertIn(storekeeper, self.manager.storekeepers)
        self.assertEqual(storekeeper.manager, self.manager)
        self.assertIn("Иван Петров", result)

    def test_appoint_storekeeper_different_warehouse(self):
        other_wh = Warehouse("Склад СПб")
        storekeeper = Storekeeper("Пётр", "Иванов", "СПб", None, other_wh)
        
        with self.assertRaises(WarehouseError) as cm:
            self.manager.appoint_storekeeper(storekeeper)
        self.assertIn("одном складе", str(cm.exception))

    def test_appoint_storekeeper_already_apppointed(self):
        storekeeper = Storekeeper("Мария", "Козлова", "Москва", None, self.warehouse)
        self.manager.appoint_storekeeper(storekeeper)
        
        with self.assertRaises(EmployeeAlreadyAppointed):
            self.manager.appoint_storekeeper(storekeeper)

    def test_appoint_loader_success(self):
        loader = Loader("Дмитрий", "Соколов", "Москва", "dima@wh.ru", self.warehouse)
        result = self.manager.appoint_loader(loader)
        
        self.assertIn(loader, self.manager.loaders)
        self.assertEqual(loader.manager, self.manager)
        self.assertIn("Дмитрий Соколов", result)

    def test_appoint_loader_different_warehouse(self):
        other_wh = Warehouse("Филиал")
        loader = Loader("Сергей", "Волков", "Екб", None, other_wh)
        
        with self.assertRaises(WarehouseError):
            self.manager.appoint_loader(loader)

    def test_assign_loader_location_success(self):
        loader = Loader("Олег", "Новиков", "Москва", None, self.warehouse)
        self.manager.appoint_loader(loader)
        
        location = Location("A1")
        self.warehouse.add_location(location)
        
        self.manager.assign_loader_location(loader, location)
        self.assertIn(location, loader.locations)

    def test_assign_loader_location_not_managed(self):
        loader = Loader("Виктор", "Павлов", "Москва", None, self.warehouse)
        location = Location("B2")
        
        with self.assertRaises(WarehouseError) as cm:
            self.manager.assign_loader_location(loader, location)
        self.assertIn("не под вашим управлением", str(cm.exception))

    def test_register_order(self):
        order = Order(customer=None)  
        result = self.manager.register_order(order)
        
        self.assertIn(order, self.manager.managed_orders)
        self.assertEqual(result, order)

    def test_assign_storekeeper_to_order_success(self):

        storekeeper = Storekeeper("Анна", "Сидорова", "Москва", None, self.warehouse)
        self.manager.appoint_storekeeper(storekeeper)
        
        order = Order(customer=None)
        self.manager.register_order(order)
  
        result = self.manager.assign_storekeeper(order, storekeeper)
        
        self.assertEqual(order.status, OrderStatus.READY)
        self.assertIn("собран", result)

    def test_assign_storekeeper_order_already_processing(self):
        storekeeper = Storekeeper("Игорь", "Морозов", "Москва", None, self.warehouse)
        self.manager.appoint_storekeeper(storekeeper)
        
        order = Order(customer=None)
        order.status = OrderStatus.PICKING  
        self.manager.register_order(order)
        
        with self.assertRaises(OrderAlreadyExist):
            self.manager.assign_storekeeper(order, storekeeper)

    def test_assign_storekeeper_not_managed(self):
        storekeeper = Storekeeper("Елена", "Васильева", "Москва", None, self.warehouse)
        order = Order(customer=None)
        
        with self.assertRaises(WarehouseError):
            self.manager.assign_storekeeper(order, storekeeper)

    def test_order_status(self):
        order = Order(customer=None)
        self.manager.register_order(order)
        self.assertEqual(self.manager.order_status(order), OrderStatus.CREATED)

    def test_total_orders(self):
        self.manager.register_order(Order(customer=None))
        self.manager.register_order(Order(customer=None))
        self.assertEqual(self.manager.total_orders(), 2)

    def test_full_integration_pick_order(self):
        product = Product("Яблоки", "P001", 100, 1, Category.FOOD, UOM.KILOGRAM)
        self.warehouse.register_product(product)
        
        batch = Batch(product, "B001", 10)
        location = Location("F1")
        bin_obj = Bin("F1-01", BinType.FRIDGE, 100)
        location.add_bin(bin_obj)
        self.warehouse.add_location(location)
        
        storekeeper = Storekeeper("Павел", "Фёдоров", "Москва", None, self.warehouse)
        self.manager.appoint_storekeeper(storekeeper)
        storekeeper.assign_location(location)
        storekeeper.receive_batch(location, batch)
        

        order = Order(customer=None)
        order.add_item(product, 5)
        self.manager.register_order(order)
        
        self.manager.assign_storekeeper(order, storekeeper)
        
        self.assertEqual(order.status, OrderStatus.READY)
        self.assertEqual(bin_obj.total_qty("P001"), 5)  

    def test_info(self):
        info = self.manager.info()
        self.assertEqual(info["name"], "Алексей Смирнов")
        self.assertIn("id", info)
        self.assertTrue(info["active"])
        self.assertEqual(info["warehouse"], "Склад Москва")
