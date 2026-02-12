from enum import Enum
class PublicationType(Enum):
    JOURNAL = "Журнал"
    CONFERENCE = "Конференция"
    BOOK_CHAPTER = "Глава книги"
    OTHER = "Другое"