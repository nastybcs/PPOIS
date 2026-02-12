import datetime
class Credit:
    def __init__(self, course, date_time, location, examiner):
        self.course = course
        self.date_time = date_time
        self.location = location
        self.examiner = examiner  
        self.passed = True
    def set_result(self, student, passed):
        self.passed = passed
        student.add_credit_result(self.course, passed, self.date_time)
        