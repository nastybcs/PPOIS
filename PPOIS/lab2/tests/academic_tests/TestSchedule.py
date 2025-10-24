import unittest
import datetime
from infrastructure.schedule import Schedule
from infrastructure.campus import Campus
from infrastructure.building import Building
from infrastructure.room import Room
from infrastructure.location import Location
from people.teacher import Teacher
from academics.course import Course
from academics.group import Group
from infrastructure.activity_type import ActivityType
from exceptions.errors import *

class TestSchedule(unittest.TestCase):
    def setUp(self):
        self.campus = Campus("Main Campus", "123 University St")
        self.building = Building("Engineering", "ENG", self.campus)
        self.campus.add_building(self.building)
        self.room = Room("101", 2, self.building)  
        self.building.add_room(self.room)
        self.location = Location(self.campus, self.building, self.room)


        self.teacher = Teacher("John", "Doe", "jdoe@example.com", "T01", None)
        self.course = Course("CS101", "Intro to CS", self.teacher, max_students=3)


        self.group = Group("G1", None, None, None, None)
        self.group.students = ["Student1", "Student2"]

        self.schedule = Schedule()

    def test_add_entry_success(self):
        
        self.schedule.add_entry(
            name="Lecture 1",
            activity_type=ActivityType.LECTURE,
            date_time=datetime.datetime(2025, 10, 22, 10, 0),
            duration=60,
            location=self.location,
            teacher=self.teacher,
            course=self.course,
            groups=[self.group]
        )
        self.assertEqual(len(self.schedule.entries), 1)
        self.assertEqual(self.schedule.entries[0]["name"], "Lecture 1")

    def test_check_room_capacity_overflow(self):
        self.group.students.append("Student3")
        with self.assertRaises(CapacityError):
            self.schedule.check_room_capacity(
                self.location, ActivityType.LECTURE, groups=[self.group]
            )

    def test_location_conflict(self):
        date_time = datetime.datetime(2025, 10, 22, 10, 0)

        self.schedule.add_entry(
            name="Lecture 1",
            activity_type=ActivityType.LECTURE,
            date_time=date_time,
            duration=60,
            location=self.location,
            teacher=self.teacher,
            course=self.course,
            groups=[self.group]
        )

        with self.assertRaises(LocationConflictedError):
            self.schedule.add_entry(
                name="Lecture 2",
                activity_type=ActivityType.LECTURE,
                date_time=date_time + datetime.timedelta(minutes=30),
                duration=60,
                location=self.location,
                teacher=self.teacher,
                course=self.course,
                groups=[self.group]
            )

