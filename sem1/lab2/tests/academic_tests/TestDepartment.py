import unittest
from academics.department import Department
from academics.faculty import Faculty
from people.teacher import Teacher
from academics.course import Course

class TestDepartment(unittest.TestCase):
    def setUp(self):
        
        self.faculty = Faculty("Engineering", "ENG001")
        self.department = Department("CS Dept", self.faculty)
        self.teacher = Teacher("John", "Doe", "john.doe@univ.com", "T001", self.department)
        self.course = Course("CS101", "Intro to Programming", self.teacher)

    def test_department_initialization(self):

        self.assertEqual(self.department.name, "CS Dept")
        self.assertEqual(self.department.faculty, self.faculty)
        self.assertEqual(self.department.teachers, [])
        self.assertEqual(self.department.courses, [])

    def test_add_teacher(self):
        
        self.department.add_teacher(self.teacher)
        self.assertIn(self.teacher, self.department.teachers)
        self.assertEqual(len(self.department.teachers), 1)

    def test_add_teacher_duplicate(self):
        
        self.department.add_teacher(self.teacher)
        initial_count = len(self.department.teachers)
        self.department.add_teacher(self.teacher)  
        self.assertEqual(len(self.department.teachers), initial_count)  
        self.assertEqual(self.department.teachers.count(self.teacher), 1)  

    def test_add_multiple_teachers(self):
        
        teacher2 = Teacher("Jane", "Smith", "jane@univ.com", "T002", self.department)
        self.department.add_teacher(self.teacher)
        self.department.add_teacher(teacher2)
        self.assertEqual(len(self.department.teachers), 2)
        self.assertIn(self.teacher, self.department.teachers)
        self.assertIn(teacher2, self.department.teachers)

    def test_add_course(self):
        
        self.department.add_course(self.course)
        self.assertIn(self.course, self.department.courses)
        self.assertEqual(len(self.department.courses), 1)

    def test_add_course_duplicate(self):
        
        self.department.add_course(self.course)
        initial_count = len(self.department.courses)
        self.department.add_course(self.course)  
        self.assertEqual(len(self.department.courses), initial_count)  
        self.assertEqual(self.department.courses.count(self.course), 1)  

    def test_add_multiple_courses(self):

        course2 = Course("CS102", "Data Structures", self.teacher)
        self.department.add_course(self.course)
        self.department.add_course(course2)
        self.assertEqual(len(self.department.courses), 2)
        self.assertIn(self.course, self.department.courses)
        self.assertIn(course2, self.department.courses)

    def test_department_without_faculty(self):
        department = Department("Math Dept", None)
        self.assertEqual(department.name, "Math Dept")
        self.assertIsNone(department.faculty)
        self.assertEqual(department.teachers, [])
        self.assertEqual(department.courses, [])