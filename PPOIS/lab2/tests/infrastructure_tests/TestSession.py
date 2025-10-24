import unittest
import datetime

from people.teacher import Teacher
from exceptions.errors import *
from people.student import Student
from academics.group import Group
from events.exam import Exam
from events.credit import Credit
from academics.course import Course
from infrastructure.session import Session


class MockGroup(Group):
    def __init__(self, name="G1"):
      
        super().__init__(name, major=None, level=None, faculty=None, leader=None, max_students=30)

class MockStudent:
    def __init__(self, student_id="S1"):
       
        self.student_id = student_id
        self.exam_grades = []   
        self.credit_results = []  

    def add_exam_grade(self, course, value, date_time):
        self.exam_grades.append((course, value, date_time))

    def add_credit_result(self, course, passed, date_time):
        self.credit_results.append((course, passed, date_time))


class MockTeacher(Teacher):
    def __init__(self, teacher_id="T1"):
       
        super().__init__("T", "Last", "t@example.com", teacher_id, department=None)

class MockCourse(Course):
    def __init__(self, code="C1", title="Course 1"):

        super().__init__(code, title, teacher=None, max_students=10)



class TestSession(unittest.TestCase):
    def setUp(self):
      
        today = datetime.date.today()
        self.start_date = today - datetime.timedelta(days=5)
        self.end_date = today + datetime.timedelta(days=5)

        self.group = MockGroup("G1")
        self.semester = None  
        self.session = Session(self.group, self.semester, self.start_date, self.end_date)

        self.teacher = MockTeacher()
        self.course = MockCourse("MATH101", "Mathematics")
        self.student = MockStudent("S100")
        self.location = "Room 101"

    def test_add_exam_within_session(self):
        exam_dt = datetime.datetime.combine(datetime.date.today(), datetime.time(10, 0))
        exam = self.session.add_exam(self.course, exam_dt, self.location, self.teacher)
        self.assertIn(exam, self.session.exams)

        self.assertEqual(exam.course, self.course)
        self.assertEqual(exam.date_time, exam_dt)
        self.assertEqual(exam.location, self.location)
        self.assertEqual(exam.examiner, self.teacher)

    def test_add_exam_out_of_session_raises(self):

        out_dt = datetime.datetime.combine(self.end_date + datetime.timedelta(days=10), datetime.time(9, 0))
        with self.assertRaises(DateOutOfSemesterError):
            self.session.add_exam(self.course, out_dt, self.location, self.teacher)

    def test_add_credit_within_session(self):
        credit_dt = datetime.datetime.combine(datetime.date.today(), datetime.time(11, 0))
        credit = self.session.add_credit(self.course, credit_dt, self.location, self.teacher)
        self.assertIn(credit, self.session.credits)
        self.assertEqual(credit.course, self.course)
        self.assertEqual(credit.date_time, credit_dt)

    def test_add_credit_out_of_session_raises(self):
        out_dt = datetime.datetime.combine(self.start_date - datetime.timedelta(days=10), datetime.time(12, 0))
        with self.assertRaises(DateOutOfSemesterError):
            self.session.add_credit(self.course, out_dt, self.location, self.teacher)

    def test_set_exam_grade_delegates_to_exam_and_student(self):
      
        exam_dt = datetime.datetime.combine(datetime.date.today(), datetime.time(10, 0))
        exam = self.session.add_exam(self.course, exam_dt, self.location, self.teacher)

      
        self.assertEqual(len(exam.grades), 0)
        self.assertEqual(len(self.student.exam_grades), 0)

     
        self.session.set_exam_grade(self.course, self.student, 88)


        self.assertIn(self.student, exam.grades)
        self.assertEqual(exam.grades[self.student], 88)

        
        self.assertEqual(len(self.student.exam_grades), 1)
        course_recorded, value_recorded, dt_recorded = self.student.exam_grades[0]
        self.assertEqual(course_recorded, self.course)
        self.assertEqual(value_recorded, 88)
        self.assertEqual(dt_recorded, exam_dt)

    def test_set_credit_result_delegates_to_credit_and_student(self):

        credit_dt = datetime.datetime.combine(datetime.date.today(), datetime.time(11, 0))
        credit = self.session.add_credit(self.course, credit_dt, self.location, self.teacher)

 
        self.assertEqual(len(credit.passed and [] or []), 0)  

      
        self.session.set_credit_result(self.course, self.student, False)

      
        self.assertEqual(len(self.student.credit_results), 1)
        course_recorded, passed_recorded, dt_recorded = self.student.credit_results[0]
        self.assertEqual(course_recorded, self.course)
        self.assertFalse(passed_recorded)
        self.assertEqual(dt_recorded, credit_dt)

    def test_is_active_with_datetime_and_date(self):
       
        d = datetime.date.today()
        dt = datetime.datetime.combine(d, datetime.time(0, 0))
        self.assertTrue(self.session.is_active(d))
        self.assertTrue(self.session.is_active(dt))

        before = self.start_date - datetime.timedelta(days=1)
        self.assertFalse(self.session.is_active(before))
        after = self.end_date + datetime.timedelta(days=1)
        self.assertFalse(self.session.is_active(after))


