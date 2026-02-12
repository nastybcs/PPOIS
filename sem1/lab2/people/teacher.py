from people.person import Person
class Teacher(Person):
    def __init__(self, first_name, last_name, email, teacher_id, department):
        super().__init__(first_name, last_name, email)
        self.teacher_id = teacher_id
        self.department = department
    def join_lab(self, lab):
        lab.add_member(self)
        if not hasattr(self, "labs"):
            self.labs = []
        self.labs.append(lab)