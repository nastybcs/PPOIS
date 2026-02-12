
import unittest
from core.product import Product
from staff.storekeeper import Storekeeper
from storage.warehouse_module import Warehouse
from storage.location import Location
from storage.bin import Bin
from storage.batch import Batch
from storage.shelf import Shelf
from orders.order import Order
from enums.product_category import Category
from enums.uom import UOM
from enums.order_status import OrderStatus
from enums.bin_type import BinType
from exceptions.errors import (
    LocationAlreadyAssigned, WarehouseError)



class TestStorekeeper(unittest.TestCase):

    def setUp(self):
        self.warehouse = Warehouse("TestWarehouse")
        self.storekeeper = Storekeeper(
            "Иван", "Иванов", "Москва", "ivan@test.ru", self.warehouse
        )

   
    def test_init_manager_default_none(self):
        self.assertIsNone(self.storekeeper.manager)

 
    def test_assign_location_duplicate_raises_error(self):
        location = Location("A1")
        self.storekeeper.assign_location(location)
        with self.assertRaises(LocationAlreadyAssigned):
            self.storekeeper.assign_location(location)  

    
    def test_receive_batch_no_access_raises_error(self):
        loc = Location("B1")
        product = Product("Яблоки", "P1", 100, 1, Category.FOOD, UOM.KILOGRAM)
        batch = Batch(product, "B001", 10)
        with self.assertRaises(WarehouseError) as cm:
            self.storekeeper.receive_batch(loc, batch)  
        self.assertIn("нет доступа", str(cm.exception))

    # Строка 30: pick — нет доступа
    def test_pick_no_access_raises_error(self):
        loc = Location("C1")
        shelf = Shelf("C1-01", BinType.STANDARD)
        loc.add_bin(shelf)
        product = Product("Молоко", "P2", 80, 1)
        with self.assertRaises(WarehouseError):
            self.storekeeper.pick(loc, shelf, product, 1) 

    
    def test_pick_order_not_created_raises_value_error(self):
        order = Order(customer=None)
        order.status = OrderStatus.PICKING 
        with self.assertRaises(ValueError) as cm:
            self.storekeeper.pick_order(order)  
        self.assertEqual(str(cm.exception), "Заказ уже в обработке")


    def test_total_qty_sums_across_locations(self):
        product = Product("Кофе", "P4", 300, 0.2)
        self.warehouse.register_product(product)

        loc1 = Location("L1")
        bin1 = Bin("B1", BinType.STANDARD, 100)
        loc1.add_bin(bin1)
        batch1 = Batch(product, "B1", 30)
        bin1.receive_batch(batch1)
        self.storekeeper.assign_location(loc1)

        loc2 = Location("L2")
        bin2 = Bin("B2", BinType.STANDARD, 100)
        loc2.add_bin(bin2)
        batch2 = Batch(product, "B2", 20)
        bin2.receive_batch(batch2)
        self.storekeeper.assign_location(loc2)

        total = self.storekeeper.total_qty(product)  
        self.assertEqual(total, 50)  

   
    def test_full_flow_receive_and_pick_success(self):
        product = Product("Хлеб", "P5", 50, 0.5)
        self.warehouse.register_product(product)

        loc = Location("F1")
        bin_obj = Bin("F1-01", BinType.STANDARD, 1000)
        loc.add_bin(bin_obj)
        self.warehouse.add_location(loc)
        self.storekeeper.assign_location(loc)

        batch = Batch(product, "BATCH-X", 15)
        self.storekeeper.receive_batch(loc, batch)  

        order = Order(customer=None)
        order.add_item(product, 10)
        result = self.storekeeper.pick_order(order) 

        self.assertTrue(result)
        self.assertEqual(order.status, OrderStatus.READY)
        self.assertEqual(bin_obj.total_qty("P5"), 5)  
