from enum import Enum
class OrderStatus(Enum):
    CREATED = "создан"
    PICKING = "сборка"
    READY = "готов к доставке"
    IN_DELIVERY = "в доставке"
    DELIVERED = "доставлено"
    CANCELLED = "отменено"