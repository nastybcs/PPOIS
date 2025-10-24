from academics.course import Course
from people.teacher import Teacher
from people.student import Student
from academics.group import Group
from academics.major import Major
from exceptions.errors import *
import unittest


class MockStudent(Student):
    def __init__(self, student_id="S01"):

        group = Group("G1", None, None, None, None)
        super().__init__("John", "Doe", "john@example.com", student_id, group)

class MockTeacher(Teacher):
    def __init__(self):
        super().__init__("Jane", "Smith", "jsmith@example.com", "T01", None)

class MockCourse(Course):
    def __init__(self, code="CS101", title="Intro CS"):
        teacher = MockTeacher()
        super().__init__(code, title, teacher)

class TestMajor(unittest.TestCase):
    def setUp(self):
        self.major = Major("Computer Science", "CS")
        self.student = MockStudent("S01")
        self.teacher = MockTeacher()
        self.course = MockCourse()

    def test_add_and_remove_student(self):
        self.major.add_student(self.student)
        self.assertIn(self.student, self.major.students)
        removed = self.major.remove_student(self.student)
        self.assertTrue(removed)
        self.assertNotIn(self.student, self.major.students)

    def test_remove_student_not_found(self):
        with self.assertRaises(StudentNotFoundError):
            self.major.remove_student(self.student)

    def test_add_and_list_courses(self):
        self.major.add_course(self.course)
        self.assertIn(self.course, self.major.courses)
        course_titles = self.major.list_courses()
        self.assertIn(self.course.title, course_titles)

    def test_add_and_list_teachers(self):
        self.major.add_teacher(self.teacher)
        self.assertIn(self.teacher, self.major.teachers)
        teacher_names = self.major.list_teachers()
        self.assertIn(f"{self.teacher.first_name} {self.teacher.last_name}", teacher_names)

