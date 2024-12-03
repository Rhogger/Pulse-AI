from enum import Enum


class SessionStatus(str, Enum):
    ACTIVE = "active"
    PROCESSING = "processing"
    IDLE = "idle"
    CLOSED = "closed"
