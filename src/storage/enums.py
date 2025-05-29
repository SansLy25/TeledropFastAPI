from enum import Enum, auto

class Permission(Enum):
    READ = auto()
    WRITE = auto()
    CHANGE = auto()