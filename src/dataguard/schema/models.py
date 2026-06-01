from dataclasses import dataclass, field
from typing import Any


@dataclass
class ColumnSchema:
    name: str
    type: str
    required: bool = False
    min: float | None = None
    max: float | None = None
    pattern: str | None = None
    min_length: int | None = None
    max_length: int | None = None
    format: str | None = None
    values: list[Any] | None = None
    # Reserved for future matching behavior; current validators remain case-sensitive.
    case_sensitive: bool = True
    true_values: list[str] | None = None
    false_values: list[str] | None = None


@dataclass
class Schema:
    name: str
    version: str
    strict: bool = True
    columns: list[ColumnSchema] = field(default_factory=list)
