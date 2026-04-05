import enum

class RoleEnum(str, enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    
class ReservationStatus(str, enum.Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"

class ReservationSeatStatus(str, enum.Enum):
    AVAILABLE = "AVAILABLE"
    PENDING = "PENDING"
    BOOKED = "BOOKED"
    CANCELLED = "CANCELLED"