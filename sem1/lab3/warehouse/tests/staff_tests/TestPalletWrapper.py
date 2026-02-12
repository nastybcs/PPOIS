import unittest
from staff.pallet_wrapper import PalletWrapper
from storage.pallet import Pallet
from storage.warehouse_module import Warehouse
from exceptions.errors import  WarehouseError


class TestPalletWrapper(unittest.TestCase):
    def setUp(self):
        self.warehouse = Warehouse("Тестовый Склад")
        self.wrapper = PalletWrapper("Игорь", "Игорев", "ул. Складская, 5", "igor@mail.com", self.warehouse)
        self.pallet = Pallet("P-001")

    def test_wrap_pallet_success(self):
        result = self.wrapper.wrap_pallet(self.pallet)
        self.assertIn("обёрнута плёнкой", result)
        self.assertEqual(self.wrapper.wrapped_pallets, 1)

    def test_wrap_pallet_already_stacked_raises(self):
        self.pallet.stack() 
        with self.assertRaises(WarehouseError):
            self.wrapper.wrap_pallet(self.pallet)

    def test_wrap_invalid_object_raises(self):
        not_a_pallet = "Это не паллета"
        with self.assertRaises(ValueError):
            self.wrapper.wrap_pallet(not_a_pallet)


