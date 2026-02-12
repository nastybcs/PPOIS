import unittest
from people.leader import Leader
from academics.group import Group
from academics.major import Major
from academics.academy_level import AcademyLevel

class TestLeader(unittest.TestCase):
    def setUp(self):

        major = Major("CS", "CS101")
        level = AcademyLevel(1)
        group = Group("CS-01", major, level, faculty=None, leader=None)
        self.leader = Leader("Иван", "Иванов", "ivan@uni.ru", student_id=1, group=group)

    def test_add_task(self):
        self.leader.add_task("Сделать отчёт")
        self.assertEqual(len(self.leader.tasks), 1)
        self.assertEqual(self.leader.tasks[0]["task"], "Сделать отчёт")
        self.assertFalse(self.leader.tasks[0]["completed"])

    def test_complete_task_success(self):
        self.leader.add_task("Сдать проект")
        result = self.leader.complete_task("Сдать проект")
        self.assertTrue(result)
        self.assertTrue(self.leader.tasks[0]["completed"])

    def test_complete_task_not_found(self):
        self.leader.add_task("Сдать проект")
        with self.assertRaises(Exception):
            self.leader.complete_task("Не существующая задача")

    def test_task_list_empty(self):
        self.assertEqual(self.leader.task_list(), "Задач нет")

    def test_task_list_with_tasks(self):
        self.leader.add_task("Сдать проект")
        self.leader.add_task("Сделать отчёт")
        self.leader.complete_task("Сдать проект")
        expected = "Список задач\nСдать проект : Выполнено\nСделать отчёт : В процессе\n"
        self.assertEqual(self.leader.task_list(), expected)

if __name__ == "__main__":
    unittest.main()
