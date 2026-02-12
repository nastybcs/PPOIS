from enum import Enum
class AttendanceStatus(Enum):
    PRESENT = "Присутствовал"
    ABSENT = "Отсутствовал"
    EXCUSED = "Уважительная причина"