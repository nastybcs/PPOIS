import unittest
import datetime
from events.event import Event
from academics.group import Group
from people.student import Student
from exceptions.errors import *
class MockStudent(Student):
    def __init__(self, student_id="S01", group=None):
        if group is None:
            group = Group("G1", None, None, None, None)
        super().__init__("John", "Doe", "john@example.com", student_id, group)

class MockGroup(Group):
    def __init__(self, name="G1"):
        super().__init__(name, None, None, None, None)

class TestEvent(unittest.TestCase):
    def setUp(self):
        self.group1 = MockGroup("G1")
        self.group2 = MockGroup("G2")
        self.student1 = MockStudent("S01", self.group1)
        self.student2 = MockStudent("S02", self.group2)
        self.event_date = datetime.datetime(2025, 10, 22, 10, 0)
        self.event = Event("Science Fair", self.event_date, location=None, organiser=None, groups=[self.group1])

    def test_add_attendee_success(self):
        self.event.add_attendee(self.student1)
        self.assertIn(self.student1, self.event.attendees)

    def test_add_attendee_not_invited(self):
        with self.assertRaises(GroupNotInvitedError):
            self.event.add_attendee(self.student2)

    def test_remove_student(self):
        self.event.add_attendee(self.student1)
        self.event.remove_student(self.student1)
        self.assertNotIn(self.student1, self.event.attendees)

    def test_cancel_event(self):
        self.event.cancel()
        self.assertTrue(self.event.is_cancelled)


