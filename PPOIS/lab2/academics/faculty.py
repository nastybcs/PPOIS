from exceptions.errors import *
class Faculty:
    def __init__(self, name, faculty_id):
        self.name = name
        self.faculty_id = faculty_id
        self.groups = []
        self.majors = []
        self.teachers = []
        self.dean = None

    def get_students_by_level(self, year):
        students = []
        for group in self.groups:
            if group.level.year == year:
                students.extend(group.students)
        return students

    def remove_student(self, student):
        for group in self.groups:
            if student in group.students:
                group.students.remove(student)
                return True
        raise StudentNotFoundError(
            f"{student.first_name} {student.last_name} не найден в факультете {self.name}."
        )

    def assign_dean(self, dean):
        self.dean = dean
        dean.faculty = self

    def add_teacher(self, teacher):
        self.teachers.append(teacher)

    def add_group(self, group):
        self.groups.append(group)