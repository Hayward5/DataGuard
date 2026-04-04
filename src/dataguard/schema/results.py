from dataclasses import dataclass
from typing import Any, Literal


@dataclass
class ValidationResult:
    row: int
    column: str
    value: Any
    level: Literal["PASS", "WARNING", "ERROR"]
    code: str
    message: str
