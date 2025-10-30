import unittest
from datetime import datetime  
from staff.cleaner import Cleaner
from storage.location import Location
from storage.warehouse_module import Warehouse


class TestCleaner(unittest.TestCase):

    def setUp(self):
        self.warehouse = Warehouse("Test Warehouse")
        self.location = Location("A1")
        self.warehouse.add_location(self.location)

        self.cleaner = Cleaner(
            first_name="Анна",
            last_name="Иванова",
            address="Москва, Ленина, 10",
            email="anna@example.com",  
            warehouse=self.warehouse
        )

    def test_init(self):
        self.assertEqual(self.cleaner.first_name, "Анна")
        self.assertEqual(self.cleaner.last_name, "Иванова")
        self.assertEqual(self.cleaner.full_name(), "Анна Иванова")
        self.assertEqual(self.cleaner.warehouse, self.warehouse)
        self.assertTrue(self.cleaner.is_active)
        self.assertEqual(self.cleaner.locations_cleaned, [])

    def test_clean_location_adds_entry(self):
        result = self.cleaner.clean_location(self.location)

        self.assertEqual(len(self.cleaner.locations_cleaned), 1)
        location_name, timestamp = self.cleaner.locations_cleaned[0]
        self.assertEqual(location_name, "A1")
        self.assertIsInstance(timestamp, datetime)
        self.assertAlmostEqual(
            timestamp.timestamp(),
            datetime.now().timestamp(),
            delta=1
        )
        self.assertIn("Локация A1 очищена уборщиком Анна Иванова", result)

    def test_clean_location_multiple_times(self):
        self.cleaner.clean_location(self.location)
        self.cleaner.clean_location(self.location)

        self.assertEqual(len(self.cleaner.locations_cleaned), 2)
        names = [entry[0] for entry in self.cleaner.locations_cleaned]
        self.assertEqual(names, ["A1", "A1"])

    def test_clean_different_locations(self):
        location2 = Location("B2")
        self.warehouse.add_location(location2)

        self.cleaner.clean_location(self.location)
        self.cleaner.clean_location(location2)

        names = [entry[0] for entry in self.cleaner.locations_cleaned]
        self.assertEqual(set(names), {"A1", "B2"})

    def test_clean_location_after_termination(self):
        self.cleaner.terminate()
        result = self.cleaner.clean_location(self.location)

        self.assertEqual(len(self.cleaner.locations_cleaned), 1)
        self.assertFalse(self.cleaner.is_active)
        self.assertIn("Локация A1 очищена уборщиком Анна Иванова", result)

    def test_clean_location_with_different_cleaner(self):
        cleaner2 = Cleaner(
            first_name="Пётр",
            last_name="Петров",
            address="СПб, Невский, 5",
            email="petr@example.com", 
            warehouse=self.warehouse
        )
        result = cleaner2.clean_location(self.location)

        self.assertIn("Локация A1 очищена уборщиком Пётр Петров", result)
