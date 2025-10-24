class Document:
    def __init__(self, type, student):
        self.student = student
        self.type = type
        self.status = "Ожидает"

    def mark_ready(self):
        self.status = "Готово"

    def mark_rejected(self):
        self.status = "Отклонено"