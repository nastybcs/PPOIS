from people.person import Person
from academics.student_grades import StudentGrades
from academics.student_debts import StudentDebts
from academics.student_scholarship import StudentScholarship
from academics.student_attendance import StudentAttendance
from events.document import Document

class Student(Person):
    def __init__(self, first_name, last_name, email, student_id, group, is_budget=True):
        super().__init__(first_name, last_name, email)
        self.student_id = student_id
        self.group = group
        self.major = group.major 
        self.is_budget = is_budget
        self.is_expelled = False
        self.student_grades = StudentGrades(self)
        self.student_debts = StudentDebts(self)
        self.student_scholarship = StudentScholarship(self)
        self.student_attendance = StudentAttendance(self)

    def add_grade(self, grade): self.student_grades.add_grade(grade)
    def add_exam_grade(self, course, value, date_time): self.student_grades.add_exam_grade(course, value, date_time)
    def add_credit_result(self, course, passed, date_time): 
        self.student_grades.add_credit_result(course, passed, date_time)
    def calculate_session_scholarship(self, session): return self.student_scholarship.calculate_session_scholarship(session)
    def request_document(self, document_type, doc_secretary):
        document = Document(document_type, self)
        doc_secretary.receive_document_request(document)
    
    def expel(self):
        self.is_expelled = True
        if self.group: self.group.remove_student(self)
        if self.major: self.major.remove_student(self)
        self.group = None
        self.major = None
    def join_lab(self, lab):
        lab.add_member(self)
        if not hasattr(self, "labs"):
            self.labs = []
        self.labs.append(lab)