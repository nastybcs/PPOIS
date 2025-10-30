
import unittest

from core.product import Product
from storage.batch import Batch
from storage.stock import Stock
from enums.product_category import Category
from exceptions.errors import BatchError, InsufficientStockError


class TestStock(unittest.TestCase):

    def setUp(self):
        self.product = Product("Milk", "P001", 70, 1.0, Category.FOOD, "LITER")
        self.stock = Stock()



    def test_init_creates_empty_storage(self):
        self.assertEqual(self.stock.storage, {})

  

    def test_receive_adds_batch_to_new_product(self):
        batch = Batch(self.product, "B001", 100)
        self.stock.receive(batch)
        self.assertIn("P001", self.stock.storage)
        self.assertEqual(len(self.stock.storage["P001"]), 1)
        self.assertEqual(self.stock.storage["P001"][0], batch)

    def test_receive_adds_to_existing_product(self):
        batch1 = Batch(self.product, "B002", 50)
        batch2 = Batch(self.product, "B003", 30)
        self.stock.receive(batch1)
        self.stock.receive(batch2)
        self.assertEqual(len(self.stock.storage["P001"]), 2)

    def test_receive_raises_if_batch_id_duplicate(self):
        batch1 = Batch(self.product, "B004", 20)
        batch2 = Batch(self.product, "B004", 40)  
        self.stock.receive(batch1)
        with self.assertRaises(BatchError) as cm:
            self.stock.receive(batch2)
        self.assertIn("уже принята", str(cm.exception))

    def test_total_qty_sums_all_batches(self):
        batch1 = Batch(self.product, "B005", 20)
        batch2 = Batch(self.product, "B006", 30)
        self.stock.receive(batch1)
        self.stock.receive(batch2)
        self.assertEqual(self.stock.total_qty("P001"), 50)

    def test_total_qty_returns_zero_if_no_product(self):
        self.assertEqual(self.stock.total_qty("UNKNOWN"), 0)

    def test_total_qty_returns_zero_if_empty_batches(self):
        batch = Batch(self.product, "B007", 0)
        self.stock.receive(batch)
        self.assertEqual(self.stock.total_qty("P001"), 0)


    def test_pick_removes_quantity_from_first_batch(self):
        batch1 = Batch(self.product, "B008", 40)
        batch2 = Batch(self.product, "B009", 60)
        self.stock.receive(batch1)
        self.stock.receive(batch2)

        picked = self.stock.pick("P001", 30)
        self.assertEqual(picked, 30)
        self.assertEqual(batch1.quantity, 10)  
        self.assertEqual(batch2.quantity, 60)
        self.assertEqual(len(self.stock.storage["P001"]), 2)

    def test_pick_spills_to_next_batch(self):
        batch1 = Batch(self.product, "B010", 20)
        batch2 = Batch(self.product, "B011", 50)
        self.stock.receive(batch1)
        self.stock.receive(batch2)

        picked = self.stock.pick("P001", 60)
        self.assertEqual(picked, 60)
        self.assertEqual(batch1.quantity, 0)
        self.assertEqual(batch2.quantity, 10)  
        self.assertEqual(len(self.stock.storage["P001"]), 1) 

    def test_pick_removes_empty_batches(self):
        batch = Batch(self.product, "B012", 25)
        self.stock.receive(batch)
        self.stock.pick("P001", 25)
        self.assertEqual(self.stock.storage.get("P001"), [])  
    def test_pick_raises_if_insufficient_stock(self):
        batch = Batch(self.product, "B013", 10)
        self.stock.receive(batch)
        with self.assertRaises(InsufficientStockError) as cm:
            self.stock.pick("P001", 20)
        self.assertIn("Недостаточно товара", str(cm.exception))

    def test_pick_handles_zero_quantity_request(self):
        batch = Batch(self.product, "B014", 100)
        self.stock.receive(batch)
        picked = self.stock.pick("P001", 0)
        self.assertEqual(picked, 0)
        self.assertEqual(batch.quantity, 100)

    def test_pick_removes_all_batches_if_all_taken(self):
        batch1 = Batch(self.product, "B015", 30)
        batch2 = Batch(self.product, "B016", 20)
        self.stock.receive(batch1)
        self.stock.receive(batch2)
        self.stock.pick("P001", 50)
        self.assertEqual(self.stock.storage.get("P001"), [])
