import unittest
from datetime import datetime, timedelta
from events.course_project import CourseProject
from people.student import Student
from people.teacher import Teacher
from academics.grade import Grade
from academics.group import Group

class MockStudent(Student):
    def __init__(self, student_id="S01"):
       
        group = Group("G1", None, None, None, None)
        super().__init__("John", "Doe", "john@example.com", student_id, group)

class MockTeacher(Teacher):
    def __init__(self):
        super().__init__("Jane", "Smith", "jsmith@example.com", "T01", None)

class TestCourseProject(unittest.TestCase):
    
    def setUp(self):
        self.student = MockStudent()
        self.supervisor = MockTeacher()
        start_date = datetime.now()
        due_date = start_date + timedelta(days=7)
        self.project = CourseProject("AI Project", self.student, self.supervisor, start_date, due_date)

    def test_start_project(self):
        self.project.start()
        self.assertEqual(self.project.status.name, "IN_PROGRESS")

    def test_submit_project(self):
        self.project.start()
        self.project.submit()
        self.assertEqual(self.project.status.name, "COMPLETED")

    def test_submit_project_not_started(self):
        with self.assertRaises(Exception):
            self.project.submit()

    def test_grade_project(self):
        self.project.start()
        self.project.submit()
        self.project.grade_project(95)
        self.assertEqual(self.project.grade, 95)
        self.assertEqual(self.project.status.name, "GRADED")
        self.assertTrue(any(isinstance(g, Grade) and g.value == 95 for g in self.student.student_grades.grades))

    def test_grade_project_not_completed(self):
        self.project.start()
        with self.assertRaises(Exception):
            self.project.grade_project(85)

