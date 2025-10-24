from people.person import Person
class DocumentSecretary(Person):
    def __init__(self, first_name, last_name, email, secretary_id, faculty):
        super().__init__(first_name, last_name, email)
        self.secretary_id = secretary_id
        self.faculty = faculty
        self.documents = []

    def receive_document_request(self, document):
        self.documents.append(document)

    def process_documents(self):
        for doc in self.documents:
            if doc.status == "Ожидает":
                doc.mark_ready()