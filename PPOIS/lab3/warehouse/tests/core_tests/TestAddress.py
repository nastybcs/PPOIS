import unittest
from core.address import Address

class TestAddress(unittest.TestCase):
    def test_create_address(self):
        addr = Address(city="Moscow", street="Lenina", house_num="10A")
        self.assertEqual(addr.city, "Moscow")
        self.assertEqual(addr.street, "Lenina")
        self.assertEqual(addr.house_num, "10A")

    def test_full_address(self):
        addr = Address(city="Moscow", street="Lenina", house_num="10A")
        self.assertEqual(addr.full_address(), "Moscow, Lenina, 10A")

    def test_short_address(self):
        addr = Address(city="Moscow", street="Lenina", house_num="10A")
        self.assertEqual(addr.short_address(), "Lenina, 10A")
