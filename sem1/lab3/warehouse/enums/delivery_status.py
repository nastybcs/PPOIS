from enum import Enum

class DeliveryStatus(Enum):
    PENDING = "в ожидании"
    ASSIGNED = "назначена"
    IN_TRANSIT = "в пути"
    DELIVERED = "доставлено"
    CANCELLED = "отменено"