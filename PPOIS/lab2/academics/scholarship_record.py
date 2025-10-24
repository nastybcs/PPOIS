class ScholarshipRecord:
    def __init__(self, scholarship_type, student, session, amount=None):
        self.scholarship_type = scholarship_type
        self.amount = amount or scholarship_type.value
        self.student = student
        self.session = session