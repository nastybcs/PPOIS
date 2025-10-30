
import unittest
from datetime import date, timedelta

from core.product import Product
from storage.batch import Batch
from storage.location import Location
from storage.bin import Bin
from enums.bin_type import BinType
from enums.product_category import Category
from exceptions.errors import WarehouseError

class TestLocation(unittest.TestCase):

    def setUp(self):
        self.location = Location("A1")

        self.food_product = Product("Milk", "P001", 70, 1.0, Category.FOOD, "LITER")
        self.chem_product = Product("Acid", "P002", 100, 0.5, Category.CHEMICAL, "LITER")

    
    def test_add_bin_success(self):
        bin_obj = Bin("BIN-01", BinType.STANDARD)
        self.location.add_bin(bin_obj)
        self.assertIn("BIN-01", self.location.bins)
        self.assertEqual(self.location.bins["BIN-01"], bin_obj)

    def test_add_bin_raises_if_duplicate_code(self):
        bin_obj = Bin("BIN-01", BinType.STANDARD)
        self.location.add_bin(bin_obj)
        with self.assertRaises(WarehouseError) as cm:
            self.location.add_bin(bin_obj)
        self.assertIn("уже есть", str(cm.exception))

    def test_get_bins_returns_bin(self):
        bin_obj = Bin("BIN-02", BinType.FRIDGE)
        self.location.add_bin(bin_obj)
        result = self.location.get_bins("BIN-02")
        self.assertEqual(result, bin_obj)

    def test_get_bins_raises_if_not_found(self):
        with self.assertRaises(WarehouseError) as cm:
            self.location.get_bins("UNKNOWN")
        self.assertIn("не найдена", str(cm.exception))
    def test_total_qty_sums_across_bins(self):
        bin1 = Bin("B1", BinType.STANDARD)
        bin2 = Bin("B2", BinType.STANDARD)
        self.location.add_bin(bin1)
        self.location.add_bin(bin2)

        batch1 = Batch(self.food_product, "B001", 30)
        batch2 = Batch(self.food_product, "B002", 20)
        bin1.receive_batch(batch1)
        bin2.receive_batch(batch2)

        total = self.location.total_qty("P001")
        self.assertEqual(total, 50)

    def test_total_qty_zero_if_no_product(self):
        bin_obj = Bin("B3", BinType.STANDARD)
        self.location.add_bin(bin_obj)
        self.assertEqual(self.location.total_qty("UNKNOWN"), 0)

    
    def test_auto_assign_bin_picks_standard_for_food(self):
        standard_bin = Bin("STD-01", BinType.STANDARD)
        fridge_bin = Bin("FR-01", BinType.FRIDGE)
        self.location.add_bin(standard_bin)
        self.location.add_bin(fridge_bin)

        batch = Batch(self.food_product, "B003", 40)
        best = self.location.auto_assign_bin(batch)
        self.assertEqual(best, standard_bin)  
    def test_auto_assign_bin_picks_fridge_only_for_food(self):
        fridge_bin = Bin("FR-01", BinType.FRIDGE)
        self.location.add_bin(fridge_bin)

        batch = Batch(self.food_product, "B004", 30)
        best = self.location.auto_assign_bin(batch)
        self.assertEqual(best, fridge_bin)

    def test_auto_assign_bin_skips_fridge_for_chemical(self):
        fridge_bin = Bin("FR-01", BinType.FRIDGE)
        standard_bin = Bin("STD-01", BinType.STANDARD)
        self.location.add_bin(fridge_bin)
        self.location.add_bin(standard_bin)

        batch = Batch(self.chem_product, "B005", 30)
        best = self.location.auto_assign_bin(batch)
        self.assertEqual(best, standard_bin)

    def test_auto_assign_bin_skips_sealed_and_pallet(self):
        sealed = Bin("SEAL-01", BinType.SEALED_BOX)
        pallet = Bin("PAL-01", BinType.STACKED_PALLET)
        standard = Bin("STD-01", BinType.STANDARD)
        self.location.add_bin(sealed)
        self.location.add_bin(pallet)
        self.location.add_bin(standard)

        batch = Batch(self.food_product, "B006", 30)
        best = self.location.auto_assign_bin(batch)
        self.assertEqual(best, standard)

    def test_auto_assign_bin_raises_if_no_space(self):
        small_bin = Bin("SMALL-01", BinType.STANDARD, capacity=10)
        self.location.add_bin(small_bin)

        batch = Batch(self.food_product, "B007", 20)
        with self.assertRaises(WarehouseError) as cm:
            self.location.auto_assign_bin(batch)
        self.assertIn("Нет места", str(cm.exception))

    def test_auto_assign_bin_picks_earliest_exp(self):
        bin1 = Bin("B1", BinType.STANDARD)
        bin2 = Bin("B2", BinType.STANDARD)
        self.location.add_bin(bin1)
        self.location.add_bin(bin2)

   
        old_batch = Batch(self.food_product, "OLD", 10, date.today() - timedelta(days=5))
        bin1.receive_batch(old_batch)

    
        new_batch = Batch(self.food_product, "NEW", 10, date.today() + timedelta(days=5))
        bin2.receive_batch(new_batch)

        incoming = Batch(self.food_product, "IN", 10)
        best = self.location.auto_assign_bin(incoming)
        self.assertEqual(best, bin1)  

    def test_auto_assign_bin_ignores_bins_without_product(self):
        bin1 = Bin("B1", BinType.STANDARD)
        bin2 = Bin("B2", BinType.STANDARD)
        self.location.add_bin(bin1)
        self.location.add_bin(bin2)

 
        batch_in_bin1 = Batch(self.food_product, "B1-1", 10)
        bin1.receive_batch(batch_in_bin1)

        incoming = Batch(self.food_product, "IN", 10)
        best = self.location.auto_assign_bin(incoming)
        self.assertEqual(best, bin1)  

    def test_auto_assign_bin_raises_if_no_candidates(self):
       
        sealed = Bin("SEAL-01", BinType.SEALED_BOX)
        self.location.add_bin(sealed)

        batch = Batch(self.food_product, "B008", 10)
        with self.assertRaises(WarehouseError):
            self.location.auto_assign_bin(batch)
