import unittest
import datetime
from academics.attendance import Attendance
from academics.attendance_tracker import AttendanceTracker
from academics.attendance_status import AttendanceStatus
from people.student import Student
from academics.group import Group
from utils.max_sizes import MAX_SIZES
from academics.student_scholarship import StudentScholarship


class MockStudent(Student):
    def __init__(self):
       
        group = Group("G1", None, None, None, None)
        super().__init__("John", "Doe", "john@example.com", "S01", group)
        self.student_scholarship = StudentScholarship(self)
        self.is_expelled = False
        self.expel_called = False

    def expel(self):
        self.is_expelled = True
        self.expel_called = True

class TestAttendance(unittest.TestCase):
    def setUp(self):

        self.group = Group("G1", None, None, None, None)
        self.student = MockStudent()
        self.group.enroll_student(self.student)
        self.tracker = AttendanceTracker(self.group)
        self.schedule_entry = {"name": "Lecture 1"}

    def test_record_attendance_present(self):
        attendance = self.tracker.record(self.student, self.schedule_entry, AttendanceStatus.PRESENT)
        self.assertFalse(attendance.is_absent)

    def test_record_attendance_absent(self):
        attendance = self.tracker.record(self.student, self.schedule_entry, AttendanceStatus.ABSENT)
        self.assertTrue(attendance.is_absent)

    def test_absence_rate_calculation(self):

        self.tracker.record(self.student, self.schedule_entry, AttendanceStatus.ABSENT)
        self.tracker.record(self.student, self.schedule_entry, AttendanceStatus.ABSENT)
        self.tracker.record(self.student, self.schedule_entry, AttendanceStatus.PRESENT)
        rate = self.tracker.absence_rate(self.student)
        self.assertEqual(rate, 2/3*100)

    def test_penalty_applied_on_5_absences(self):

        for _ in range(5):
            self.tracker.record(self.student, self.schedule_entry, AttendanceStatus.ABSENT)
        self.assertEqual(self.student.student_scholarship.penalty, 0.5)
        self.assertFalse(self.student.is_expelled)

    def test_expel_on_36_absences(self):
       
        for _ in range(36):
            self.tracker.record(self.student, self.schedule_entry, AttendanceStatus.ABSENT)
        self.assertTrue(self.student.is_expelled)
        self.assertTrue(self.student.expel_called)

