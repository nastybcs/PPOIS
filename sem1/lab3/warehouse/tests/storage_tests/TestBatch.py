
import unittest
from datetime import datetime, date, timedelta

from core.product import Product
from storage.batch import Batch
from enums.uom import UOM
from enums.product_category import Category


class TestBatch(unittest.TestCase):

    def setUp(self):
        self.product = Product("Milk", "P001", 70, 1.0, Category.FOOD, UOM.LITER)

    def test_batch_init_with_exp_date(self):
        exp_date = date.today() + timedelta(days=10)
        batch = Batch(self.product, "B001", 100, exp_date)

        self.assertEqual(batch.product, self.product)
        self.assertEqual(batch.batch_id, "B001")
        self.assertEqual(batch.quantity, 100)
        self.assertEqual(batch.exp_date, exp_date)
        self.assertIsNotNone(batch.received_at)
        self.assertLess(batch.received_at, datetime.now())

    def test_batch_init_without_exp_date(self):
        batch = Batch(self.product, "B002", 50)

        self.assertEqual(batch.product, self.product)
        self.assertEqual(batch.batch_id, "B002")
        self.assertEqual(batch.quantity, 50)
        self.assertIsNone(batch.exp_date)
        self.assertIsNotNone(batch.received_at)



    def test_age_days_returns_integer_days(self):
      
        past = datetime.now() - timedelta(days=5, hours=3)
        batch = Batch(self.product, "B003", 30)
        batch.received_at = past 

        age = batch.age_days()
        self.assertEqual(age, 5) 

    def test_age_days_zero_if_just_received(self):
        batch = Batch(self.product, "B004", 20)
        age = batch.age_days()
        self.assertEqual(age, 0)  


    def test_is_expired_returns_true_if_expired(self):
        exp_date = date.today() - timedelta(days=1)
        batch = Batch(self.product, "B005", 10, exp_date)
        self.assertTrue(batch.is_expired())

    def test_is_expired_returns_false_if_not_expired(self):
        exp_date = date.today() + timedelta(days=1)
        batch = Batch(self.product, "B006", 10, exp_date)
        self.assertFalse(batch.is_expired())

    def test_is_expired_returns_false_if_no_exp_date(self):
        batch = Batch(self.product, "B007", 10)
        self.assertFalse(batch.is_expired())

