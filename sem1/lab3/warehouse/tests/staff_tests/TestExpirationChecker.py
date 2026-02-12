import unittest
from datetime import date
from staff.expiration_checker import ExpirationChecker
from exceptions.errors import WarehouseError


class DummyBatch:
    def __init__(self, name, expired=False):
        self.product = type("P", (), {"name": name, "product_id": f"id_{name}"})()
        self.batch_id = f"batch_{name}"
        self.exp_date = date(2024, 1, 1)
        self.quantity = 10
        self._expired = expired

    def is_expired(self):
        return self._expired


class DummyBin:

    def __init__(self, name="bin1"):
        self.name = name
        self.storage = {"A": []}

    def receive_batch(self, batch):
        self.storage["A"].append(batch)

    def total_qty(self, pid):
        return sum(b.quantity for b in self.storage["A"] if b.product.product_id == pid)

    def pick(self, pid, qty):
        for b in list(self.storage["A"]):
            if b.product.product_id == pid:
                b.quantity -= qty
                if b.quantity <= 0:
                    self.storage["A"].remove(b)

    def add_expired_batch(self, batch, checker):
        return f"{checker.full_name()} переместил {batch.product.name} в просроченные"


class DummyLocation:
    def __init__(self, name="loc1"):
        self.name = name
        self.bins = {"bin1": DummyBin(), "bin2": DummyBin()}


class DummyWarehouse:
    def __init__(self):
        self.locations = {"L1": DummyLocation()}


class TestExpirationChecker(unittest.TestCase):
    def setUp(self):
        self.warehouse = DummyWarehouse()
        self.checker = ExpirationChecker("Ирина", "Котова", "Москва", "irina@ex.com", self.warehouse)

    def test_scan_location_finds_expired_batches(self):
        expired = DummyBatch("молоко", expired=True)
        fresh = DummyBatch("кефир", expired=False)
        loc = self.warehouse.locations["L1"]
        loc.bins["bin1"].receive_batch(expired)
        loc.bins["bin1"].receive_batch(fresh)

        result = self.checker.scan_location(loc)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["product"], "молоко")
        self.assertIn(expired, self.checker.checked_batches)

    def test_full_report_counts_only_expired(self):
        self.checker.checked_batches = [DummyBatch("молоко", expired=True),
                                        DummyBatch("кефир", expired=False)]
        report = self.checker.full_report()
        self.assertIn("1 просроченных", report)

    def test_move_to_expired_bin_success(self):
        expired_batch = DummyBatch("сыр", expired=True)
        loc = self.warehouse.locations["L1"]
        loc.bins["bin1"].receive_batch(expired_batch)
        self.checker.checked_batches.append(expired_batch)
        expired_bin = DummyBin("expired")

        result = self.checker.move_to_expired_bin(expired_batch, expired_bin)

        self.assertIn("переместил", result)
        self.assertNotIn(expired_batch, loc.bins["bin1"].storage["A"])

    def test_move_to_expired_bin_not_found_raises(self):
        batch = DummyBatch("йогурт", expired=True)
        expired_bin = DummyBin("expired")
        with self.assertRaises(WarehouseError):
            self.checker.move_to_expired_bin(batch, expired_bin)

    def test_move_to_expired_bin_not_expired_raises(self):
        fresh_batch = DummyBatch("сок", expired=False)
        loc = self.warehouse.locations["L1"]
        loc.bins["bin1"].receive_batch(fresh_batch)
        self.checker.checked_batches.append(fresh_batch)
        expired_bin = DummyBin("expired")

        with self.assertRaises(WarehouseError):
            self.checker.move_to_expired_bin(fresh_batch, expired_bin)
