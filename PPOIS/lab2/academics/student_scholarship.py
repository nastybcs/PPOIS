from academics.scholarship_type import ScholarshipType
from academics.scholarship_record import ScholarshipRecord
class StudentScholarship:
    def __init__(self, student):
        self.student = student
        self.penalty = 1.0
        self.scholarships = []
    
    def set_penalty(self, penalty):
        self.penalty = penalty
    
    def calculate_session_scholarship(self, session):
        avg = self.student.student_grades.get_session_average(session)
        if avg is None or self.student.student_debts.academic_debts or self.student.is_expelled:
            scholarship = ScholarshipType.NONE
            amount = 0
        elif avg >= 90:
            scholarship = ScholarshipType.EXCELLENT
        elif avg >= 75:
            scholarship = ScholarshipType.GOOD
        elif avg >= 60:
            scholarship = ScholarshipType.BASIC
        else:
            scholarship = ScholarshipType.NONE
        
        base_amount = scholarship.value
        leader_bonus = 1.2 if self.student.group and self.student.group.leader == self.student else 1.0
        amount = int(base_amount * leader_bonus * self.penalty)
        
        record = ScholarshipRecord(scholarship, self.student, session, amount)
        self.scholarships.append(record)
        return scholarship