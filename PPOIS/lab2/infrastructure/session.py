from exceptions.errors import *
import datetime
from events.exam import Exam
from events.credit import Credit
class Session:
    def __init__(self,group, semester, start_date, end_date):
        self.semester = semester
        self.group = group
        self.start_date = start_date
        self.end_date = end_date
        self.exams = []
        self.credits = []

    def is_active(self, date_time):
        if isinstance(date_time, datetime.datetime):
            d = date_time.date()
        else:
            d = date_time
        return self.start_date <= d <= self.end_date
    def add_exam(self, course,date_time, location, examiner):
        if not self.is_active(date_time):
            raise DateOutOfSemesterError(
                f"Дата {date_time.date()} вне периода сессии"
            )
        exam = Exam(course, date_time, location, examiner)
        self.exams.append(exam)
        return exam
    def add_credit(self, course, date_time, location, examiner):
        if not self.is_active(date_time):
            raise DateOutOfSemesterError(
                f"Дата {date_time.date()} вне периода сессии"
            )
        credit = Credit(course, date_time,location, examiner)
        self.credits.append(credit)
        return credit
    def set_exam_grade(self, course, student, value):
        for exam in self.exams:
            if exam.course == course:
                exam.set_grade(student, value)
    def set_credit_result(self, course, student, passed):
        for credit in self.credits:
            if credit.course == course:
                credit.set_result(student, passed)