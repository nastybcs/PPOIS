from people.person import Person
class Dean(Person):
    def __init__(self, first_name, last_name, email, dean_id, faculty):
        super().__init__(first_name, last_name, email)
        self.dean_id = dean_id
        self.faculty = faculty