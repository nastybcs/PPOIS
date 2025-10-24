from exceptions.errors import *
from utils.max_sizes import MAX_SIZES
class Course:
    def __init__(self, code, title, teacher, max_students=MAX_SIZES.COURSE):
        self.code = code
        self.title = title
        self.teacher = teacher
        self.students = []
        self.max_students = max_students

    def enroll_student(self, student):
        if len(self.students) >= self.max_students:
            raise CourseFullError("Курс переполнен.")
        self.students.append(student)

    def remove_student(self, student):
        if student in self.students:
            self.students.remove(student)
            return True
        raise StudentNotFoundError(
            f"{student.first_name} {student.last_name} не найден в курсе {self.title}."
        )
