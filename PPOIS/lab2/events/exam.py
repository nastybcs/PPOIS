import datetime
class Exam:
    def __init__(self, course, date_time, location, examiner):
        self.course = course
        self.date_time = date_time
        self.location = location
        self.examiner = examiner  
        self.grades = {}
    def set_grade(self, student, value):
        self.grades[student] = value
        student.add_exam_grade(self.course, value, self.date_time)