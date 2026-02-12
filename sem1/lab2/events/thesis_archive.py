class ThesisArchive:
    def __init__(self):
        self.archived_theses = []

    def archive_thesis(self, thesis):
        if thesis.is_archived:
            raise Exception(f"Дипломная работа '{thesis.title}' уже в архиве")
        thesis.is_archived = True
        self.archived_theses.append(thesis)

    def find_theses_by_student(self, student):
        return [t for t in self.archived_theses if t.student == student]

    def find_theses_by_supervisor(self, supervisor):
        return [t for t in self.archived_theses if t.supervisor == supervisor]

    def list_all_archived(self):
        return self.archived_theses