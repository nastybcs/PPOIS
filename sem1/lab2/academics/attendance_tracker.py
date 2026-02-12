from academics.attendance import Attendance
class AttendanceTracker:
    def __init__(self, group):
        self.group = group
        self.attendances = []
    
    def record(self, student, schedule_entry, status):
        attendance = Attendance(student, schedule_entry, status)
        self.attendances.append(attendance)
        self._check_absences(student)
        return attendance
    
    def _check_absences(self, student):
        total_absences = len([a for a in self.attendances if a.student == student and a.is_absent])
        if total_absences >= 36:
            student.expel()
        elif total_absences >= 5:
            student.student_scholarship.set_penalty(0.5)
    
    def absence_rate(self, student):
        total = len([a for a in self.attendances if a.student == student])
        absent = len([a for a in self.attendances if a.student == student and a.is_absent])
        return absent / total * 100 if total else 0