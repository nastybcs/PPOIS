from enum import Enum
class RouteStatus(Enum):
    PLANNED = "запланирован"
    IN_PROGRESS = "в пути"
    COMPLETED = "завершён"
    CANCELLED = "отменён"