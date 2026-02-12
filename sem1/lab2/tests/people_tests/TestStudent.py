import unittest
import datetime
from academics.faculty import Faculty
from academics.major import Major
from academics.academy_level import AcademyLevel
from academics.group import Group
from people.teacher import Teacher
from academics.course import Course
from infrastructure.semester import Semester
from infrastructure.session import Session
from people.student import Student
from infrastructure.campus import Campus
from infrastructure.building import Building
from infrastructure.room import Room
from infrastructure.location import Location
from people.document_secretary import DocumentSecretary
from events.research_lab import ResearchLab
from academics.grade import Grade
from academics.student_grades import StudentGrades
from academics.student_debts import StudentDebts
from academics.student_attendance import StudentAttendance
from academics.student_scholarship import StudentScholarship
from academics.scholarship_type import ScholarshipType
from exceptions.errors import *


class TestStudent(unittest.TestCase):
    def setUp(self):
        self.faculty = Faculty("Engineering", "ENG001")
        self.major = Major("Computer Science", "CS")
        self.level = AcademyLevel(1)
        self.group = Group("CS1", self.major, self.level, self.faculty, None)
        self.teacher = Teacher("John", "Doe", "john.doe@univ.com", "T001", None)
        self.course = Course("CS101", "Intro to Programming", self.teacher)
        self.semester = Semester("Fall 2025", datetime.date(2025, 9, 1), datetime.date(2025, 12, 31))
        self.session = Session(self.group, self.semester, datetime.date(2025, 12, 1), datetime.date(2025, 12, 31))
        self.student = Student("Alice", "Smith", "alice@univ.com", "S001", self.group, is_budget=True)
        self.campus = Campus("Main Campus", "123 University St")
        self.building = Building("Building A", "A1", self.campus)
        self.room = Room("101", 50, self.building)
        self.location = Location(self.campus, self.building, self.room)
        self.doc_secretary = DocumentSecretary("Jane", "Doe", "jane@univ.com", "DS001", self.faculty)
        self.lab = ResearchLab("AI Lab", self.teacher)

    def test_student_initialization(self):

        self.assertEqual(self.student.first_name, "Alice")
        self.assertEqual(self.student.last_name, "Smith")
        self.assertEqual(self.student.email, "alice@univ.com")
        self.assertEqual(self.student.student_id, "S001")
        self.assertEqual(self.student.group, self.group)
        self.assertEqual(self.student.major, self.major)
        self.assertTrue(self.student.is_budget)
        self.assertFalse(self.student.is_expelled)
        self.assertIsInstance(self.student.student_grades, StudentGrades)
        self.assertIsInstance(self.student.student_debts, StudentDebts)
        self.assertIsInstance(self.student.student_scholarship, StudentScholarship)
        self.assertIsInstance(self.student.student_attendance, StudentAttendance)

    def test_add_grade(self):

        grade = Grade(self.course, 85)
        self.student.add_grade(grade)
        self.assertIn(grade, self.student.student_grades.grades)
        self.assertEqual(self.student.student_grades.average_grade(), 85)

    def test_add_grade_invalid(self):

        grade = Grade(self.course, 101)
        with self.assertRaises(InvalidGradeError):
            self.student.add_grade(grade)

    def test_add_exam_grade_passing(self):

        self.student.add_exam_grade(self.course, 75, datetime.datetime(2025, 12, 10))
        self.assertEqual(self.student.student_grades.exam_grades[-1].value, 75)
        self.assertEqual(self.student.student_grades.exam_grades[-1].course, self.course)
        self.assertNotIn(self.course, self.student.student_debts.academic_debts)

    def test_add_exam_grade_failing(self):

        self.student.add_exam_grade(self.course, 35, datetime.datetime(2025, 12, 10))
        self.assertEqual(self.student.student_grades.exam_grades[-1].value, 35)
        self.assertIn(self.course, self.student.student_debts.academic_debts)

    def test_add_credit_result_passed(self):

        self.student.add_credit_result(self.course, True, datetime.datetime(2025, 12, 10))
        self.assertTrue(self.student.student_grades.credit_results[-1].passed)
        self.assertNotIn(self.course, self.student.student_debts.academic_debts)

    def test_add_credit_result_failed(self):

        self.student.add_credit_result(self.course, False, datetime.datetime(2025, 12, 10))
        self.assertFalse(self.student.student_grades.credit_results[-1].passed)
        self.assertIn(self.course, self.student.student_debts.academic_debts)

    def test_calculate_session_scholarship_excellent(self):

        self.group.enroll_student(self.student)
        date_time = datetime.datetime(2025, 12, 10)
        self.session.add_exam(self.course, date_time, self.location, self.teacher)
        self.student.add_exam_grade(self.course, 95, date_time)
        scholarship = self.student.calculate_session_scholarship(self.session)
        self.assertEqual(scholarship, ScholarshipType.EXCELLENT)
        self.assertEqual(self.student.student_scholarship.scholarships[-1].amount, 10000)

    def test_calculate_session_scholarship_good(self):

        self.group.enroll_student(self.student)
        date_time = datetime.datetime(2025, 12, 10)
        self.session.add_exam(self.course, date_time, self.location, self.teacher)
        self.student.add_exam_grade(self.course, 80, date_time)
        scholarship = self.student.calculate_session_scholarship(self.session)
        self.assertEqual(scholarship, ScholarshipType.GOOD)
        self.assertEqual(self.student.student_scholarship.scholarships[-1].amount, 5000)

    def test_calculate_session_scholarship_basic(self):

        self.group.enroll_student(self.student)
        date_time = datetime.datetime(2025, 12, 10)
        self.session.add_exam(self.course, date_time, self.location, self.teacher)
        self.student.add_exam_grade(self.course, 65, date_time)
        scholarship = self.student.calculate_session_scholarship(self.session)
        self.assertEqual(scholarship, ScholarshipType.BASIC)
        self.assertEqual(self.student.student_scholarship.scholarships[-1].amount, 2000)

    def test_calculate_session_scholarship_none(self):

        self.group.enroll_student(self.student)
        date_time = datetime.datetime(2025, 12, 10)
        self.session.add_exam(self.course, date_time, self.location, self.teacher)
        self.student.add_exam_grade(self.course, 50, date_time)
        scholarship = self.student.calculate_session_scholarship(self.session)
        self.assertEqual(scholarship, ScholarshipType.NONE)
        self.assertEqual(self.student.student_scholarship.scholarships[-1].amount, 0)

    def test_calculate_session_scholarship_leader_bonus(self):

        self.group.enroll_student(self.student)
        self.group.assign_leader(self.student)
        date_time = datetime.datetime(2025, 12, 10)
        self.session.add_exam(self.course, date_time, self.location, self.teacher)
        self.student.add_exam_grade(self.course, 80, date_time)
        scholarship = self.student.calculate_session_scholarship(self.session)
        self.assertEqual(scholarship, ScholarshipType.GOOD)
        self.assertEqual(self.student.student_scholarship.scholarships[-1].amount, int(5000 * 1.2))

    def test_calculate_session_scholarship_with_penalty(self):

        self.group.enroll_student(self.student)
        self.student.student_scholarship.set_penalty(0.5)
        date_time = datetime.datetime(2025, 12, 10)
        self.session.add_exam(self.course, date_time, self.location, self.teacher)
        self.student.add_exam_grade(self.course, 80, date_time)
        scholarship = self.student.calculate_session_scholarship(self.session)
        self.assertEqual(scholarship, ScholarshipType.GOOD)
        self.assertEqual(self.student.student_scholarship.scholarships[-1].amount, int(5000 * 0.5))

    def test_calculate_session_scholarship_expelled(self):

        self.group.enroll_student(self.student)
        date_time = datetime.datetime(2025, 12, 10)
        self.session.add_exam(self.course, date_time, self.location, self.teacher)
        self.student.expel()
        self.student.add_exam_grade(self.course, 95, date_time)
        scholarship = self.student.calculate_session_scholarship(self.session)
        self.assertEqual(scholarship, ScholarshipType.NONE)
        self.assertEqual(self.student.student_scholarship.scholarships[-1].amount, 0)

    def test_request_document(self):

        document_type = "Transcript"
        self.student.request_document(document_type, self.doc_secretary)
        self.assertEqual(len(self.doc_secretary.documents), 1)
        self.assertEqual(self.doc_secretary.documents[0].type, document_type)
        self.assertEqual(self.doc_secretary.documents[0].status, "Ожидает")

    def test_expel(self):

        self.group.enroll_student(self.student)
        self.major.add_student(self.student)
        self.student.expel()
        self.assertTrue(self.student.is_expelled)
        self.assertIsNone(self.student.group)
        self.assertIsNone(self.student.major)
        self.assertNotIn(self.student, self.group.students)
        self.assertNotIn(self.student, self.major.students)

    def test_join_lab(self):

        self.student.join_lab(self.lab)
        self.assertIn(self.lab, self.student.labs)
        self.assertIn(self.student, self.lab.members)

    def test_student_attendance_record_absence(self):

        self.student.student_attendance.record_absence()
        self.assertEqual(self.student.student_attendance.absences, 1)
        self.assertEqual(self.student.student_scholarship.penalty, 1.0)  

    def test_student_attendance_multiple_absences(self):
 
        for _ in range(5):
            self.student.student_attendance.record_absence()
        self.assertEqual(self.student.student_attendance.absences, 5)
        self.assertEqual(self.student.student_scholarship.penalty, 0.5)

    def test_student_attendance_expel(self):
       
        self.group.enroll_student(self.student)
        for _ in range(36):
            self.student.student_attendance.record_absence()
        self.assertTrue(self.student.is_expelled)
        self.assertIsNone(self.student.group)

