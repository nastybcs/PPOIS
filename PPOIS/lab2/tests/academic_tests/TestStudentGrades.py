import unittest
import datetime
from academics.student_grades import StudentGrades
from people.student import Student
from academics.group import Group
from academics.faculty import Faculty
from academics.major import Major
from academics.academy_level import AcademyLevel
from academics.course import Course
from infrastructure.session import Session
from academics.grade import Grade
from academics.exam_grade import ExamGrade
from academics.credit_grade import CreditGrade
from exceptions.errors import *

class TestStudentGrades(unittest.TestCase):
    def setUp(self):
        self.major = Major("Информатика", "INF01")
        self.faculty = Faculty("Факультет ИТ", "IT01")
        self.level = AcademyLevel(1)
        self.group = Group("Группа 101", self.major, self.level, self.faculty, leader=None)
        self.course = Course("CS101", "Программирование", teacher=None)
        self.student = Student("Анна", "Петрова", "anna@example.com", "ST01", self.group)
        self.grades = StudentGrades(self.student)

    def test_add_grade_success(self):
        grade = Grade(self.course, 85)
        self.grades.add_grade(grade)
        self.assertEqual(len(self.grades.grades), 1)
        self.assertEqual(self.grades.grades[0].value, 85)

    def test_add_grade_invalid_raises_error(self):
        grade = Grade(self.course, 150)
        with self.assertRaises(InvalidGradeError):
            self.grades.add_grade(grade)

    def test_average_grade_calculation(self):
        self.grades.add_grade(Grade(self.course, 80))
        self.grades.add_grade(Grade(self.course, 100))
        avg = self.grades.average_grade()
        self.assertEqual(avg, 90)

    def test_average_grade_empty_returns_none(self):
        self.assertIsNone(self.grades.average_grade())

    def test_has_failed_courses_true(self):
        self.grades.add_grade(Grade(self.course, 30))
        self.assertTrue(self.grades.has_failed_courses())

    def test_has_failed_courses_false(self):
        self.grades.add_grade(Grade(self.course, 70))
        self.assertFalse(self.grades.has_failed_courses())

    def test_get_course_grade_returns_correct_values(self):
        grade1 = Grade(self.course, 95)
        self.grades.add_grade(grade1)
        values = self.grades.get_course_grade("CS101")
        self.assertEqual(values, [95])

    def test_get_course_grade_returns_empty_list(self):
        values = self.grades.get_course_grade("MATH101")
        self.assertEqual(values, [])

    def test_add_exam_grade_creates_exam_grade(self):
        date_time = datetime.datetime.now()
        self.grades.add_exam_grade(self.course, 85, date_time)
        self.assertIsInstance(self.grades.exam_grades[0], ExamGrade)
        self.assertEqual(self.grades.exam_grades[0].value, 85)

    def test_add_credit_result_creates_credit_grade(self):
        date_time = datetime.datetime.now()
        self.grades.add_credit_result(self.course, True, date_time)
        self.assertIsInstance(self.grades.credit_results[0], CreditGrade)
        self.assertTrue(self.grades.credit_results[0].passed)

    def test_get_session_average_returns_correct_value(self):

        semester = type('MockSemester', (), {})()  
        session = Session(self.group, semester, datetime.date(2024, 1, 1), datetime.date(2024, 3, 1))
        exam_date = datetime.datetime(2024, 1, 15)
        session.add_exam(self.course, exam_date, None, None)
        self.grades.add_exam_grade(self.course, 80, exam_date)
        self.grades.add_exam_grade(self.course, 100, exam_date)
        avg = self.grades.get_session_average(session)
        self.assertEqual(avg, 90)

    def test_get_session_average_no_exams_returns_none(self):
        semester = type('MockSemester', (), {})()
        session = Session(self.group, semester, datetime.date(2024, 1, 1), datetime.date(2024, 3, 1))
        self.assertIsNone(self.grades.get_session_average(session))



