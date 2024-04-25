from enum import Enum

class BaseStatusCode(Enum):
    BAD_REQUEST = 400
    CONFLICT = 409
    INTERNAL_ERROR = 525

    def __str__(self):
        return f"({self.value})"
    