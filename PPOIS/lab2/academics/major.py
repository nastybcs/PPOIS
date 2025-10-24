from exceptions.errors import *
class Major:
    def __init__(self, name, code):
        self.name = name
        self.code = code
        self.courses = []
        self.students = []
        self.teachers = []
    def add_course(self, course):
        if course not in self.courses:
            self.courses.append(course)

    def list_courses(self):
        return [course.title for course in self.courses]

    def add_student(self, student):
        if student not in self.students:
            self.students.append(student)

    def remove_student(self, student):
        if student in self.students:
            self.students.remove(student)
            return True
        raise StudentNotFoundError(
            f"{student.first_name} {student.last_name} не найден на специальности {self.name}."
        )

    def add_teacher(self, teacher):
        if teacher not in self.teachers:
            self.teachers.append(teacher)

    def list_teachers(self):
        return [f"{t.first_name} {t.last_name}" for t in self.teachers]