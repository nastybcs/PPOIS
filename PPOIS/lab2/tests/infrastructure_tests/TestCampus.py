import unittest
from infrastructure.campus import Campus
from infrastructure.building import Building
from exceptions.errors import *
class MockBuilding(Building):
    def __init__(self, name="B1", building_code="B1"):
        super().__init__(name, building_code, campus=None)

class TestCampus(unittest.TestCase):
    def setUp(self):
        self.campus = Campus("Main Campus", "123 University St")
        self.building1 = MockBuilding("B1", "B1")
        self.building2 = MockBuilding("B2", "B2")

    def test_add_building(self):
        self.campus.add_building(self.building1)
        self.assertIn(self.building1, self.campus.buildings)
        self.assertIn("B1", self.campus.list_of_buildings())

    def test_add_building_no_duplicates(self):
        self.campus.add_building(self.building1)
        self.campus.add_building(self.building1)
        self.assertEqual(self.campus.buildings.count(self.building1), 1)

    def test_remove_building_success(self):
        self.campus.add_building(self.building1)
        self.campus.remove_building(self.building1)
        self.assertNotIn(self.building1, self.campus.buildings)

    def test_remove_building_not_found(self):
        with self.assertRaises(BuildingNotFoundError):
            self.campus.remove_building(self.building2)


