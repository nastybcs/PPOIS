import unittest

from people.teacher import Teacher
from people.student import Student
from academics.group import Group
from academics.faculty import Faculty
from people.dean import Dean
from academics.academy_level import AcademyLevel
from exceptions.errors import *
class MockStudent(Student):
    def __init__(self, student_id="S01", level=None):
        group = Group("G1", None, level, None, None)
        super().__init__("John", "Doe", "john@example.com", student_id, group)

class MockDean(Dean):
    def __init__(self):
        super().__init__("Jane", "Smith", "jsmith@example.com", "D01", None)

class MockTeacher(Teacher):
    def __init__(self):
        super().__init__("Alice", "Brown", "abrown@example.com", "T01", None)

class TestFaculty(unittest.TestCase):
    def setUp(self):
        self.faculty = Faculty("Engineering", "F01")
        self.level1 = AcademyLevel(1)
        self.level2 = AcademyLevel(2)

        # Создаем группы
        self.group1 = Group("G1", None, self.level1, self.faculty, None)
        self.group2 = Group("G2", None, self.level2, self.faculty, None)
        self.faculty.add_group(self.group1)
        self.faculty.add_group(self.group2)

        # Студенты
        self.student1 = MockStudent("S01", self.level1)
        self.student2 = MockStudent("S02", self.level2)
        self.group1.enroll_student(self.student1)
        self.group2.enroll_student(self.student2)

        # Преподаватели и декан
        self.teacher = MockTeacher()
        self.dean = MockDean()

    def test_add_teacher(self):
        self.faculty.add_teacher(self.teacher)
        self.assertIn(self.teacher, self.faculty.teachers)

    def test_assign_dean(self):
        self.faculty.assign_dean(self.dean)
        self.assertEqual(self.faculty.dean, self.dean)
        self.assertEqual(self.dean.faculty, self.faculty)

    def test_get_students_by_level(self):
        students_level1 = self.faculty.get_students_by_level(1)
        students_level2 = self.faculty.get_students_by_level(2)
        self.assertIn(self.student1, students_level1)
        self.assertNotIn(self.student2, students_level1)
        self.assertIn(self.student2, students_level2)

    def test_remove_student_success(self):
        result = self.faculty.remove_student(self.student1)
        self.assertTrue(result)
        self.assertNotIn(self.student1, self.group1.students)

    def test_remove_student_not_found(self):
        unknown_student = MockStudent("S03", self.level1)
        with self.assertRaises(StudentNotFoundError):
            self.faculty.remove_student(unknown_student)

