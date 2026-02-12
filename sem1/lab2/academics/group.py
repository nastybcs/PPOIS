from utils.max_sizes import MAX_SIZES
from exceptions.errors import *
from academics.attendance_tracker import AttendanceTracker

class Group:
    def __init__(self, name, major, level, faculty, leader, max_students=MAX_SIZES.GROUP):
        self.name = name
        self.major = major
        self.level = level
        self.faculty = faculty
        self.leader = leader
        self.students = []
        self.max_students = max_students

    def enroll_student(self, student):
        if len(self.students) >= self.max_students:
            raise GroupFullError("Группа переполнена.")
        self.students.append(student)
        student.group = self
        if hasattr(self, "major") and self.major:
            try:
                self.major.add_student(student)
            except Exception:
                pass
        if not hasattr(self, 'attendance_tracker'):
            self.attendance_tracker = AttendanceTracker(self)

    def assign_leader(self, student):
        if student not in self.students:
            raise StudentNotFoundError(
                f"Студент {student.first_name} {student.last_name} не состоит в группе {self.name}"
            )
        self.leader = student

    def remove_leader(self):
        self.leader = None

    def remove_student(self, student):
        if student in self.students:
            self.students.remove(student)
            return True
        raise StudentNotFoundError(
            f"{student.first_name} {student.last_name} не найден в группе {self.name}."
        )