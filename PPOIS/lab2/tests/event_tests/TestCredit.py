import unittest
import datetime
from academics.course import Course
from events.credit import Credit
from academics.student_debts import StudentDebts
from people.student import Student
from academics.group import Group

class MockStudent(Student):
    def __init__(self):
        
        group = Group("G1", None, None, None, None)
        super().__init__("John", "Doe", "john@example.com", "S01", group)
        self.student_debts = StudentDebts(self)
        self.expel_called = False
    def expel(self):
        self.expel_called = True

class MockCourse(Course):
    def __init__(self):
        teacher = None
        super().__init__("CS101", "Intro CS", teacher)

class TestCredit(unittest.TestCase):
    def setUp(self):
        self.student = MockStudent()
        self.course = MockCourse()
        self.date_time = datetime.datetime(2025, 10, 22, 10, 0)
        self.credit = Credit(self.course, self.date_time, location=None, examiner=None)

    def test_set_credit_passed(self):
        self.credit.set_result(self.student, passed=True)
        self.assertTrue(self.credit.passed)
        self.assertEqual(len(self.student.student_debts.academic_debts), 0)
        self.assertFalse(self.student.expel_called)

    def test_set_credit_failed_adds_debt(self):
        self.credit.set_result(self.student, passed=False)
        self.assertFalse(self.credit.passed)
        self.assertIn(self.course, self.student.student_debts.academic_debts)
        self.assertFalse(self.student.expel_called)


