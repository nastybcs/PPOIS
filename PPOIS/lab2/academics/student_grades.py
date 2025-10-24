from exceptions.errors import *
from academics.exam_grade import ExamGrade
from academics.credit_grade import CreditGrade
class StudentGrades:
    def __init__(self, student):
        self.student = student
        self.grades = []
        self.exam_grades = []
        self.credit_results = []

    def add_grade(self, grade):
        if grade.value < 0 or grade.value > 100:
            raise InvalidGradeError("Оценка должна быть от 1 до 100.")
        self.grades.append(grade)
    def average_grade(self):
        if not self.grades:
            return None
        return sum(grade.value for grade in self.grades) / len(self.grades)
    def has_failed_courses(self, threshold=40):
        for grade in self.grades:
            if grade.value < threshold:
                return True
        return False

    def get_course_grade(self, course_code):
        course_grades = []
        for grade in self.grades:
            if grade.course.code == course_code:
                course_grades.append(grade.value)
        return course_grades
    def add_exam_grade(self, course, value, date_time): 
        grade = ExamGrade(course, value, date_time)
        self.exam_grades.append(grade)
        if value < 40:  
            self.student.student_debts.add_debt(course)
    def add_credit_result(self, course, passed, date_time):
        result = CreditGrade(course, passed, date_time)
        self.credit_results.append(result)
        if not passed:                                            
            self.student.student_debts.add_debt(course)
    def get_session_average(self, session):
        exam_grades = [g for g in self.exam_grades 
                   if any(e.date_time == g.date_time for e in session.exams)]
        return sum(g.value for g in exam_grades) / len(exam_grades) if exam_grades else None