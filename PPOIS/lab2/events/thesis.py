from exceptions.errors import *
class Thesis:
    def __init__(self, title, student, supervisor, submission_date=None, grade=None):
        self.title = title
        self.student = student
        self.supervisor = supervisor
        self.submission_date = submission_date
        self.grade = grade
        self.is_archived = False

    def submit(self, submission_date):
        self.submission_date = submission_date

    def set_grade(self, grade):
        if grade < 0 or grade > 100:
            raise InvalidGradeError("Оценка должна быть от 0 до 100")
        self.grade = grade