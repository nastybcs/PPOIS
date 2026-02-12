import unittest
from events.course_project import CourseProject
from people.student import Student
from people.teacher import Teacher
from events.research_lab import ResearchLab
from academics.group import Group

class MockStudent(Student):
    def __init__(self, student_id="S01"):
       
        group = Group("G1", None, None, None, None)
        super().__init__("John", "Doe", "john@example.com", student_id, group)

class MockTeacher(Teacher):
    def __init__(self):
        super().__init__("Jane", "Smith", "jsmith@example.com", "T01", None)

class MockProject(CourseProject):
    def __init__(self, student, supervisor):
        from datetime import datetime, timedelta
        start_date = datetime.now()
        due_date = start_date + timedelta(days=7)
        super().__init__("Project 1", student, supervisor, start_date, due_date)

class TestResearchLab(unittest.TestCase):
    def setUp(self):
        self.supervisor = MockTeacher()
        self.lab = ResearchLab("AI Lab", self.supervisor)
        self.student = MockStudent()
        self.project = MockProject(self.student, self.supervisor)

    def test_add_member(self):
        self.lab.add_member(self.student)
        self.assertIn(self.student, self.lab.members)
        self.assertIn(self.lab, self.student.labs)

    def test_remove_member(self):
        self.lab.add_member(self.student)
        self.lab.remove_member(self.student)
        self.assertNotIn(self.student, self.lab.members)
        self.assertNotIn(self.lab, getattr(self.student, "labs", []))

    def test_add_project(self):
        self.lab.add_project(self.project)
        self.assertIn(self.project, self.lab.projects)

    def test_add_member_no_duplicates(self):
        self.lab.add_member(self.student)
        self.lab.add_member(self.student)
        self.assertEqual(self.lab.members.count(self.student), 1)

    def test_add_project_no_duplicates(self):
        self.lab.add_project(self.project)
        self.lab.add_project(self.project)
        self.assertEqual(self.lab.projects.count(self.project), 1)

