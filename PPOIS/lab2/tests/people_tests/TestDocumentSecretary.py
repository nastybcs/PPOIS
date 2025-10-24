import unittest
from  people.document_secretary import DocumentSecretary
from  events.document import Document

class TestDocumentSecretary(unittest.TestCase):
    def setUp(self):
        self.faculty = "Факультет информатики"
        self.secretary = DocumentSecretary("Анна", "Петрова", "anna@example.com", "SEC001", self.faculty)
        self.document = Document("Заявление", "Ожидает")  

    def test_receive_document_request(self):
        initial_length = len(self.secretary.documents)
        self.secretary.receive_document_request(self.document)
        self.assertEqual(len(self.secretary.documents), initial_length + 1)
        self.assertIn(self.document, self.secretary.documents)

    def test_process_documents(self):
        self.secretary.documents.append(self.document)
        self.assertEqual(self.document.status, "Ожидает")
        self.secretary.process_documents()
        self.assertEqual(self.document.status, "Готово") 

    def tearDown(self):
        self.secretary.documents.clear()