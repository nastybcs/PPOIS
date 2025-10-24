class Department:
    def __init__(self, name, faculty):
        self.name = name
        self.faculty = faculty
        self.teachers = []
        self.courses = []

    def add_teacher(self, teacher):
        if teacher not in self.teachers:
            self.teachers.append(teacher)

    def add_course(self, course):
        if course not in self.courses:
            self.courses.append(course)