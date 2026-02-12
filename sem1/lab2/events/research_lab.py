class ResearchLab:
    def __init__(self, name, supervisor):
        self.name = name
        self.supervisor = supervisor  
        self.members = []  
        self.projects = []  

    def add_member(self, person):
        if person not in self.members:
            self.members.append(person)
            if not hasattr(person, "labs"):
                person.labs = []
            person.labs.append(self)

    def remove_member(self, person):
        if person in self.members:
            self.members.remove(person)
            if hasattr(person, "labs"):
                person.labs.remove(self)

    def add_project(self, project):
        if project not in self.projects:
            self.projects.append(project)