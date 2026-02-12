from exceptions.errors import *
from utils.max_sizes import MAX_SIZES
class Subgroup:
    def __init__(self, name, group, max_students = MAX_SIZES.SUBGROUP):
        self.name = name
        self.group = group
        self.max_students = max_students
        self.students = []
    
    def add_student(self,student):
        if student.group != self.group:
            raise StudentNotFoundError(
                f"Студент {student.first_name} {student.last_name} не состоит в группе {self.group.name}"
            )
        if len(self.students) >= self.max_students:
            raise SubGroupFullError("Подгруппа переполнена.")
        self.students.append(student)
        student.subgroup = self

    def remove_student(self, student):
        if student not in self.students:
            raise StudentNotFoundError(f"Студент {student} не найден в подгруппе {self.name}.")
        self.students.remove(student)
        student.subgroup = None

