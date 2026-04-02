import enum

class RoleEnum(str, enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"

class ReservationSeatStatus(str, enum.Enum):
    AVAILABLE = "AVAILABLE"
    PENDING = "PENDING"
    BOOKED = "BOOKED"
    CANCELLED = "CANCELLED"