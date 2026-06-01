from dataclasses import dataclass
from typing import Any, Literal


@dataclass
class ValidationResult:
    row: int
    column: str
    value: Any
    # WARNING is reserved for report compatibility; validators currently emit PASS or ERROR.
    level: Literal["PASS", "WARNING", "ERROR"]
    code: str
    message: str
