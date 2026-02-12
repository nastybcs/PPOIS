from people.student import Student
from exceptions.errors import *
class Leader(Student):
    def __init__(self, first_name, last_name, email, student_id, group):
        super().__init__(first_name, last_name, email, student_id, group)
        self.tasks = []

    def add_task(self, description):
        self.tasks.append({
            "task": description,
            "completed": False
        })

    def complete_task(self, description):
        for task in self.tasks:
            if task["task"] == description:
                task["completed"] = True
                return True
        raise TaskNotFoundError(f"Задача {description} не найдена")

    def task_list(self):
        if not self.tasks:
            return "Задач нет"
        result = "Список задач\n"
        for t in self.tasks:
            status = "Выполнено" if t["completed"] else "В процессе"
            result += f"{t['task']} : {status}\n"
        return result