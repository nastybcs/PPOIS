class StudentAttendance:
    def __init__(self, student):
        self.student = student
        self.absences = 0
    def record_absence(self):
        self.absences += 1
        if self.absences >= 36:
            self.student.expel()
        elif self.absences >= 5:
            self.student.student_scholarship.set_penalty(0.5)