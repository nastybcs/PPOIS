import unittest
from datetime import datetime, timedelta
from people.teacher import Teacher
from academics.grade import Grade
from exceptions.errors import *
from people.student import Student
from academics.group import Group
from events.exam import Exam
from academics.course import Course

class MockCourse(Course):
    def __init__(self):
        super().__init__(code="MATH101", title="Math", teacher=None)

class MockTeacher(Teacher):
    def __init__(self):
        super().__init__("Jane", "Doe", "jane@example.com", teacher_id="T1", department=None)

class MockGroup(Group):
    def __init__(self):
        super().__init__("G1", major=None, level=None, faculty=None, leader=None)

class MockStudent(Student):
    def __init__(self):
        super().__init__("John", "Smith", "john@example.com", "S1", group=MockGroup())
        self.exam_grades = []

    def add_exam_grade(self, course, value, date_time):
        self.exam_grades.append((course, value, date_time))

class TestExam(unittest.TestCase):
    def setUp(self):
        self.teacher = MockTeacher()
        self.course = MockCourse()
        self.student = MockStudent()
        self.date_time = datetime.now()
        self.exam = Exam(self.course, self.date_time, location="Room 101", examiner=self.teacher)

    def test_set_grade_adds_entry(self):

        self.exam.set_grade(self.student, 85)
        self.assertIn(self.student, self.exam.grades)
        self.assertEqual(self.exam.grades[self.student], 85)

    def test_student_add_exam_grade_called(self):

        self.exam.set_grade(self.student, 90)
        self.assertEqual(len(self.student.exam_grades), 1)
        course, value, date_time = self.student.exam_grades[0]
        self.assertEqual(course, self.course)
        self.assertEqual(value, 90)
        self.assertEqual(date_time, self.date_time)

    def test_multiple_students_grades(self):

        student2 = MockStudent()
        self.exam.set_grade(self.student, 70)
        self.exam.set_grade(student2, 95)
        self.assertEqual(self.exam.grades[self.student], 70)
        self.assertEqual(self.exam.grades[student2], 95)

