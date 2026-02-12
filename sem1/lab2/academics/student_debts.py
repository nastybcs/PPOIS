class StudentDebts:
    def __init__(self, student):
        self.student = student
        self.academic_debts = []
    def add_debt(self, course):
        if course not in self.academic_debts:
            self.academic_debts.append(course)
            if len(self.academic_debts) >= 3:
                self.student.expel()