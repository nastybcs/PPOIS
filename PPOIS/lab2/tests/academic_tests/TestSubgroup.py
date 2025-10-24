import unittest
from academics.subgroup import Subgroup
from academics.group import Group
from people.student import Student
from exceptions.errors import *

class MockGroup(Group):
    def __init__(self, name="G1"):
        super().__init__(name, major=None, level=None, faculty=None, leader=None, max_students=30)

class MockStudent(Student):
    def __init__(self, student_id="S01", group=None):
        if group is None:
            group = MockGroup()
        super().__init__("John", "Doe", "john@example.com", student_id, group)
        self.subgroup = None 

class TestSubgroup(unittest.TestCase):
    def setUp(self):
        self.group = MockGroup("G1")
        self.subgroup = Subgroup("G1-1", self.group)
        self.student1 = MockStudent("S01", self.group)
        self.student2 = MockStudent("S02", self.group)

    def test_add_student_success(self):
        self.subgroup.add_student(self.student1)
        self.assertIn(self.student1, self.subgroup.students)
        self.assertEqual(self.student1.subgroup, self.subgroup)

    def test_remove_student_success(self):
        self.subgroup.add_student(self.student1)
        self.subgroup.remove_student(self.student1)
        self.assertNotIn(self.student1, self.subgroup.students)
        self.assertIsNone(self.student1.subgroup)

    def test_remove_student_not_found(self):
        with self.assertRaises(StudentNotFoundError):
            self.subgroup.remove_student(self.student2)

    def test_subgroup_group_link(self):
        self.assertEqual(self.subgroup.group, self.group)


