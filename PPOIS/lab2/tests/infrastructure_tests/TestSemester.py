import unittest
import datetime
from infrastructure.building import Building
from infrastructure.semester import Semester
from infrastructure.location import Location
from infrastructure.campus import Campus
from infrastructure.room import Room
from infrastructure.activity_type import ActivityType
from academics.faculty import Faculty
from academics.major import Major
from academics.academy_level import AcademyLevel
from academics.group import Group
from people.teacher import Teacher
from academics.course import Course
from exceptions.errors import *


class TestSemester(unittest.TestCase):

    def setUp(self):
        self.campus = Campus("Главный кампус", "ул. Академическая, 1")
        self.building = Building("Корпус А", "A1", self.campus)
        self.room = Room("101", 30, self.building)
        self.building.add_room(self.room)
        self.location = Location(self.campus, self.building, self.room)

        self.faculty = Faculty("ФКТИ", "FKTI")
        self.major = Major("Информатика", "CS101")
        self.level = AcademyLevel(1)
        self.teacher = Teacher("Иван", "Иванов", "ivanov@uni.ru", "T001", None)
        self.group = Group("Группа 1", self.major, self.level, self.faculty, None)
        self.course = Course("CS101", "Программирование", self.teacher)

        self.semester = Semester(
            "Осенний 2025",
            datetime.date(2025, 9, 1),
            datetime.date(2025, 12, 31)
        )

    
    def test_is_active_within_dates(self):
        self.assertTrue(self.semester.is_active(datetime.date(2025, 10, 15)))

    def test_is_active_before_start(self):
        self.assertFalse(self.semester.is_active(datetime.date(2025, 8, 31)))

    def test_is_active_after_end(self):
        self.assertFalse(self.semester.is_active(datetime.date(2026, 1, 1)))

    
    def test_add_schedule_entry_success(self):
        self.semester.add_schedule_entry(
            "Лекция 1",
            ActivityType.LECTURE,
            datetime.datetime(2025, 10, 15, 10, 0),
            90,
            self.location,
            self.teacher,
            self.course,
            groups=[self.group],
        )

        self.assertEqual(len(self.semester.schedule.entries), 1)
        entry = self.semester.schedule.entries[0]
        self.assertEqual(entry["name"], "Лекция 1")
        self.assertEqual(entry["activity_type"], "Лекция")
        self.assertEqual(entry["teacher"], self.teacher)

    def test_add_schedule_entry_out_of_semester_raises(self):
        with self.assertRaises(DateOutOfSemesterError):
            self.semester.add_schedule_entry(
                "Лекция за рамками семестра",
                ActivityType.LECTURE,
                datetime.datetime(2026, 1, 5, 12, 0),
                90,
                self.location,
                self.teacher,
                self.course,
                groups=[self.group],
            )

    def test_add_schedule_entry_over_capacity_raises(self):
        big_group = self.group
        big_group.students = [f"Student{i}" for i in range(40)]

        with self.assertRaises(CapacityError):
            self.semester.add_schedule_entry(
                "Лекция переполнена",
                ActivityType.LECTURE,
                datetime.datetime(2025, 10, 15, 10, 0),
                90,
                self.location,
                self.teacher,
                self.course,
                groups=[big_group],
            )

    def test_add_schedule_entry_conflict_raises(self):
        date = datetime.datetime(2025, 10, 15, 10, 0)

        
        self.semester.add_schedule_entry(
            "Лекция 1",
            ActivityType.LECTURE,
            date,
            90,
            self.location,
            self.teacher,
            self.course,
            groups=[self.group],
        )

        
        with self.assertRaises(LocationConflictedError):
            self.semester.add_schedule_entry(
                "Лекция 2 (конфликт)",
                ActivityType.LECTURE,
                date + datetime.timedelta(minutes=30),
                60,
                self.location,
                self.teacher,
                self.course,
                groups=[self.group],
            )