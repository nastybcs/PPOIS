import unittest
import datetime
from people.student import Student
from people.person import Person
from events.thesis import Thesis
from events.thesis_archive import ThesisArchive
from academics.group import Group
from academics.major import Major
from academics.academy_level import AcademyLevel


class TestThesisAndArchive(unittest.TestCase):
    def setUp(self):
 
        major = Major("CS", "CS101")
        level = AcademyLevel(1)
        self.group = Group("CS-01", major, level, faculty=None, leader=None)


        self.student = Student("Иван", "Иванов", "ivan@uni.ru", student_id=1, group=self.group)

        self.supervisor = Person("Петр", "Петров", "petr@uni.ru")

        self.thesis = Thesis("AI Thesis", self.student, self.supervisor)

        self.archive = ThesisArchive()
    def test_submit_thesis(self):
        date = datetime.date(2025, 10, 22)
        self.thesis.submit(date)
        self.assertEqual(self.thesis.submission_date, date)

    def test_set_valid_grade(self):
        self.thesis.set_grade(95)
        self.assertEqual(self.thesis.grade, 95)

    def test_set_invalid_grade_raises(self):
        with self.assertRaises(Exception):
            self.thesis.set_grade(150)

    def test_archive_thesis(self):
        self.archive.archive_thesis(self.thesis)
        self.assertTrue(self.thesis.is_archived)
        self.assertIn(self.thesis, self.archive.archived_theses)

    def test_archive_duplicate_raises(self):
        self.archive.archive_thesis(self.thesis)
        with self.assertRaises(Exception):
            self.archive.archive_thesis(self.thesis)

    def test_find_theses_by_student(self):
        self.archive.archive_thesis(self.thesis)
        theses = self.archive.find_theses_by_student(self.student)
        self.assertIn(self.thesis, theses)

    def test_find_theses_by_supervisor(self):
        self.archive.archive_thesis(self.thesis)
        theses = self.archive.find_theses_by_supervisor(self.supervisor)
        self.assertIn(self.thesis, theses)

    def test_list_all_archived(self):
        self.archive.archive_thesis(self.thesis)
        self.assertEqual(self.archive.list_all_archived(), [self.thesis])


