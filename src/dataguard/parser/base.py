from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ParseErrorItem:
    row: int
    message: str


@dataclass
class ParseResult:
    records: list[dict[str, Any]] = field(default_factory=list)
    errors: list[ParseErrorItem] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class BaseParser(ABC):
    @abstractmethod
    def parse(self, file_path: str, encoding: str | None = None) -> ParseResult:
        raise NotImplementedError
