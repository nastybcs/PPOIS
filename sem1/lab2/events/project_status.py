from enum import Enum
class ProjectStatus(Enum):
    NOT_STARTED = "Не начат"
    IN_PROGRESS = "В процессе"
    COMPLETED = "Завершен"
    GRADED = "Оценен"