import unittest

from people.teacher import Teacher
from academics.department import Department
from academics.course import Course

class TestTeacher(unittest.TestCase):
    def setUp(self):
  
        self.department = Department(name="Компьютерные науки", faculty=None)
        
 
        self.teacher = Teacher(
            first_name="Иван",
            last_name="Иванов",
            email="ivanov@uni.ru",
            teacher_id="T001",
            department=self.department
        )
        

        self.course = Course(
            code="CS101",
            title="Программирование",
            teacher=self.teacher
        )

    def test_teacher_creation(self):
        self.assertEqual(self.teacher.first_name, "Иван")
        self.assertEqual(self.teacher.last_name, "Иванов")
        self.assertEqual(self.teacher.email, "ivanov@uni.ru")
        self.assertEqual(self.teacher.teacher_id, "T001")
        self.assertEqual(self.teacher.department, self.department)

    def test_teacher_full_name(self):
        full_name = f"{self.teacher.first_name} {self.teacher.last_name}"
        self.assertEqual(full_name, "Иван Иванов")

    def test_join_lab(self):
 
        class DummyLab:
            def __init__(self):
                self.members = []
            def add_member(self, person):
                self.members.append(person)
        
        lab = DummyLab()
        self.teacher.join_lab(lab)
        self.assertIn(self.teacher, lab.members)
        self.assertIn(lab, self.teacher.labs)

    def test_remove_course_not_in_department(self):
        new_course = Course("CS102", "Алгоритмы", self.teacher)
        with self.assertRaises(Exception):
       
            if new_course in self.teacher.department.courses:
                self.teacher.department.courses.remove(new_course)
            else:
                raise Exception("Курс не найден")

    def test_add_course_to_department(self):
        self.teacher.department.add_course(self.course)
        self.assertIn(self.course, self.teacher.department.courses)

if __name__ == "__main__":
    unittest.main()
