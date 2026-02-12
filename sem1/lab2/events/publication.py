class Publication:
    def __init__(self, title, authors, pub_type, date, venue, doi=None):
 
        self.title = title
        self.authors = authors
        self.pub_type = pub_type
        self.date = date
        self.venue = venue
        self.doi = doi

        for author in self.authors:
            if not hasattr(author, "publications"):
                author.publications = []
            author.publications.append(self)

    def list_authors(self):
        return [f"{a.first_name} {a.last_name}" for a in self.authors]