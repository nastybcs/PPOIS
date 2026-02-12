from academics.attendance_status import AttendanceStatus
class Attendance:
    def __init__(self, student, schedule_entry, status=AttendanceStatus.PRESENT):
        self.student = student
        self.schedule_entry = schedule_entry
        self.status = status
    @property
    def is_absent(self):
        return self.status == AttendanceStatus.ABSENT