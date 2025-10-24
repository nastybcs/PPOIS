import unittest
from infrastructure.building import Building
from infrastructure.room import Room
from exceptions.errors import *

class MockRoom(Room):
    def __init__(self, room_number="101", capacity=30):
        super().__init__(room_number, capacity, building=None)

class TestBuilding(unittest.TestCase):
    def setUp(self):
        self.building = Building("Main Building", "B1", campus=None)
        self.room1 = MockRoom("101", 30)
        self.room2 = MockRoom("102", 40)

    def test_add_room(self):
        self.building.add_room(self.room1)
        self.assertIn(self.room1, self.building.rooms)
        self.assertIn("101", self.building.list_of_rooms())

    def test_add_room_no_duplicates(self):
        self.building.add_room(self.room1)
        self.building.add_room(self.room1)
        self.assertEqual(self.building.rooms.count(self.room1), 1)

    def test_remove_room_success(self):
        self.building.add_room(self.room1)
        self.building.remove_room(self.room1)
        self.assertNotIn(self.room1, self.building.rooms)

    def test_remove_room_not_found(self):
        with self.assertRaises(RoomNotFoundError):
            self.building.remove_room(self.room2)


