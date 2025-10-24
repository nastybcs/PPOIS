import unittest
from academics.course import Course
from people.teacher import Teacher
from people.student import Student
from academics.group import Group
from exceptions.errors import *
class MockStudent(Student):
    def __init__(self, student_id="S01"):
        group = Group("G1", None, None, None, None)
        super().__init__("John", "Doe", "john@example.com", student_id, group)

class MockTeacher(Teacher):
    def __init__(self):
        super().__init__("Jane", "Smith", "jsmith@example.com", "T01", None)

class TestCourse(unittest.TestCase):
    def setUp(self):
        self.teacher = MockTeacher()
        self.course = Course("CS101", "Intro to CS", self.teacher, max_students=2)
        self.student1 = MockStudent("S01")
        self.student2 = MockStudent("S02")
        self.student3 = MockStudent("S03")

    def test_enroll_student_success(self):
        self.course.enroll_student(self.student1)
        self.assertIn(self.student1, self.course.students)

    def test_enroll_student_over_capacity(self):
        self.course.enroll_student(self.student1)
        self.course.enroll_student(self.student2)
        with self.assertRaises(CourseFullError):
            self.course.enroll_student(self.student3)

    def test_remove_student_success(self):
        self.course.enroll_student(self.student1)
        removed = self.course.remove_student(self.student1)
        self.assertTrue(removed)
        self.assertNotIn(self.student1, self.course.students)

    def test_remove_student_not_found(self):
        with self.assertRaises(StudentNotFoundError):
            self.course.remove_student(self.student1)

