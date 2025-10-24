from events.project_status import ProjectStatus
from academics.grade import Grade
class CourseProject:
    def __init__(self, title, student, supervisor, start_date, due_date):
        self.title = title
        self.student = student
        self.supervisor = supervisor
        self.start_date = start_date
        self.due_date = due_date
        self.status = ProjectStatus.NOT_STARTED
        self.grade = None

    def start(self):
        self.status = ProjectStatus.IN_PROGRESS

    def submit(self):
        if self.status != ProjectStatus.IN_PROGRESS:
            raise Exception("Проект нельзя сдать, пока он не начат")
        self.status = ProjectStatus.COMPLETED

    def grade_project(self, grade):
        if self.status != ProjectStatus.COMPLETED:
            raise Exception("Проект можно оценить только после сдачи")
        self.grade = grade
        self.status = ProjectStatus.GRADED

        self.student.add_grade(Grade(course=None, value=grade))