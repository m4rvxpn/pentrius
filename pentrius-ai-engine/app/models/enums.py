"""Output routing decisions from CDE Phase 1."""
from enum import Enum


class OutputRouting(str, Enum):
    DROP = "DROP"
    KEEP = "KEEP"
    BORDERLINE = "BORDERLINE"


class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


class AutoTrigger(str, Enum):
    SPAWN = "SPAWN"
    NONE = "NONE"
    MANUAL = "MANUAL"
