import unittest
from academics.major import Major
from exceptions.errors import *
from utils.max_sizes import MAX_SIZES
from academics.academy_level import AcademyLevel
from people.student import Student
from academics.group import Group
class MockStudent(Student):
    def __init__(self, student_id="S01", group=None):
        if group is None:
            group = Group("G1", None, None, None, None)
        super().__init__("John", "Doe", "john@example.com", student_id, group)

class MockMajor(Major):
    def __init__(self):
        super().__init__("Computer Science", "CS")

class TestGroup(unittest.TestCase):
    def setUp(self):
        self.major = MockMajor()
        self.level = AcademyLevel(1)
        self.group = Group("G1", self.major, self.level, None, None, max_students=2)
        self.student1 = MockStudent("S01", self.group)
        self.student2 = MockStudent("S02", self.group)
        self.student3 = MockStudent("S03", self.group)

    def test_enroll_student_success(self):
        self.group.enroll_student(self.student1)
        self.assertIn(self.student1, self.group.students)
        self.assertIn(self.student1, self.major.students)

    def test_enroll_student_over_capacity(self):
        self.group.enroll_student(self.student1)
        self.group.enroll_student(self.student2)
        with self.assertRaises(GroupFullError):
            self.group.enroll_student(self.student3)

    def test_assign_and_remove_leader(self):
        self.group.enroll_student(self.student1)
        self.group.assign_leader(self.student1)
        self.assertEqual(self.group.leader, self.student1)
        self.group.remove_leader()
        self.assertIsNone(self.group.leader)

    def test_assign_leader_not_in_group(self):
        with self.assertRaises(StudentNotFoundError):
            self.group.assign_leader(self.student1)

    def test_remove_student_success(self):
        self.group.enroll_student(self.student1)
        removed = self.group.remove_student(self.student1)
        self.assertTrue(removed)
        self.assertNotIn(self.student1, self.group.students)

    def test_remove_student_not_found(self):
        with self.assertRaises(StudentNotFoundError):
            self.group.remove_student(self.student1)


