import unittest

from academics.group import Group
from infrastructure.capacity_calculator import CapacityCalculator
from academics.subgroup import Subgroup
from people.student import Student
from infrastructure.activity_type import ActivityType
class MockStudent(Student):
    def __init__(self, student_id="S01", group=None):
        
        if group is None:
            group = Group("G1", None, None, None, None)
        super().__init__("John", "Doe", "john@example.com", student_id, group)

class MockGroup(Group):
    def __init__(self, name="G1", students=None):
        super().__init__(name, None, None, None, None)
        self.students = students or []

class MockSubgroup(Subgroup):
    def __init__(self, name="SG1", group=None, students=None):
        if group is None:
            group = MockGroup()
        super().__init__(name, group)
        self.students = students or []

class TestCapacityCalculator(unittest.TestCase):
    def setUp(self):
        self.student1 = MockStudent("S01")
        self.student2 = MockStudent("S02")
        self.student3 = MockStudent("S03")

        self.group1 = MockGroup("G1", [self.student1, self.student2])
        self.group2 = MockGroup("G2", [self.student3])

        self.subgroup = MockSubgroup("SG1", self.group1, [self.student1])

    def test_lecture_capacity(self):
        total = CapacityCalculator.calculate(ActivityType.LECTURE, groups=[self.group1, self.group2])
        self.assertEqual(total, 3)

    def test_practical_capacity(self):
        total = CapacityCalculator.calculate(ActivityType.PRACTICAL, groups=[self.group1, self.group2])
        self.assertEqual(total, 2)

    def test_lab_capacity(self):
        total = CapacityCalculator.calculate(ActivityType.LAB, subgroup=self.subgroup)
        self.assertEqual(total, 1)

    def test_no_groups_or_subgroup(self):
        self.assertEqual(CapacityCalculator.calculate(ActivityType.LECTURE, groups=[]), 0)
        self.assertEqual(CapacityCalculator.calculate(ActivityType.PRACTICAL, groups=[]), 0)
        self.assertEqual(CapacityCalculator.calculate(ActivityType.LAB, subgroup=None), 0)

