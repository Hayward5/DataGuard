# DataGuard Phase 1 Implementation Plan

> For Claude: REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Implement the DataGuard Phase 1 foundation (project scaffold + parser module with CSV/JSON/JSONL parsing + encoding detection) with unit tests.

**Architecture:** Use `DataGuard/` as project root with `src/dataguard/` package. Parsing returns `ParseResult(records, errors, metadata)`. CSV/JSON parsing focuses on robust file reading and basic validation while recording errors without crashing.

**Tech Stack:** Python 3.10+, pytest, click, PyYAML, chardet

---

### Task 1: Project scaffold and dependencies (config-only)

**Files:**
- Create: `DataGuard/pyproject.toml`
- Create: `DataGuard/requirements.txt`
- Create: `DataGuard/requirements-dev.txt`
- Create: `DataGuard/README.md`
- Create: `DataGuard/src/dataguard/__init__.py`
- Create: `DataGuard/src/dataguard/exceptions.py`

**Step 1: Create minimal pyproject.toml**

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "dataguard"
version = "0.1.0"
description = "Schema-driven CSV/JSON validator and transformer"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
  "click>=8.0",
  "PyYAML>=6.0",
  "chardet>=5.0"
]

[project.scripts]
dataguard = "dataguard.cli:main"
```

**Step 2: Create requirements files**

```text
# DataGuard/requirements.txt
click>=8.0
PyYAML>=6.0
chardet>=5.0
```

```text
# DataGuard/requirements-dev.txt
pytest>=8.0
pytest-cov
black
flake8
```

**Step 3: Create README.md (minimal)**

```markdown
# DataGuard

Schema-driven CSV/JSON validation and transformation CLI.

## Development

```bash
pytest -q
```
```

**Step 4: Create package init + exceptions**

```python
# DataGuard/src/dataguard/__init__.py
__version__ = "0.1.0"
```

```python
# DataGuard/src/dataguard/exceptions.py
class DataGuardError(Exception):
    """Base exception for DataGuard."""


class ParseError(DataGuardError):
    """Raised when parsing fails in a non-recoverable way."""
```

**Step 5: Verification (config-only exception to TDD)**

Run: `python -c "import tomllib; tomllib.load(open('DataGuard/pyproject.toml','rb'))"`
Expected: No output, exit code 0

---

### Task 2: CSV parser (basic parsing)

**Files:**
- Create: `DataGuard/src/dataguard/parser/base.py`
- Create: `DataGuard/src/dataguard/parser/csv_parser.py`
- Create: `DataGuard/tests/unit/parser/test_csv_parser.py`

**Step 1: Write failing test (basic CSV)**

```python
def test_csv_parser_reads_header_and_rows(tmp_path):
    csv_path = tmp_path / "employees.csv"
    csv_path.write_text("id,name\n1,Alice\n2,Bob\n", encoding="utf-8")

    parser = CsvParser()
    result = parser.parse(str(csv_path))

    assert result.records == [
        {"id": "1", "name": "Alice"},
        {"id": "2", "name": "Bob"},
    ]
    assert result.errors == []
    assert result.metadata["delimiter"] == ","
```

**Step 2: Run test to verify it fails**

Run: `pytest DataGuard/tests/unit/parser/test_csv_parser.py::test_csv_parser_reads_header_and_rows -v`
Expected: FAIL with ImportError or AttributeError (CsvParser missing)

**Step 3: Write minimal implementation**

```python
# DataGuard/src/dataguard/parser/base.py
from dataclasses import dataclass, field
from typing import Any
from abc import ABC, abstractmethod


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
```

```python
# DataGuard/src/dataguard/parser/csv_parser.py
import csv
from .base import BaseParser, ParseResult


class CsvParser(BaseParser):
    def parse(self, file_path: str, encoding: str | None = None) -> ParseResult:
        used_encoding = encoding or "utf-8"
        with open(file_path, "r", encoding=used_encoding, newline="") as handle:
            sample = handle.read(1024)
            handle.seek(0)
            dialect = csv.Sniffer().sniff(sample) if sample else csv.excel
            reader = csv.DictReader(handle, dialect=dialect)
            records = [row for row in reader]
        return ParseResult(records=records, errors=[], metadata={"delimiter": dialect.delimiter})
```

**Step 4: Run test to verify it passes**

Run: `pytest DataGuard/tests/unit/parser/test_csv_parser.py::test_csv_parser_reads_header_and_rows -v`
Expected: PASS

**Step 5: Commit**

```bash
git add DataGuard/src/dataguard/parser/base.py DataGuard/src/dataguard/parser/csv_parser.py DataGuard/tests/unit/parser/test_csv_parser.py
git commit -m "feat: add basic CSV parsing"
```

---

### Task 3: CSV delimiter detection and row mismatch errors

**Files:**
- Modify: `DataGuard/src/dataguard/parser/csv_parser.py`
- Modify: `DataGuard/tests/unit/parser/test_csv_parser.py`

**Step 1: Write failing tests (delimiter + mismatched columns)**

```python
def test_csv_parser_detects_semicolon_delimiter(tmp_path):
    csv_path = tmp_path / "employees.csv"
    csv_path.write_text("id;name\n1;Alice\n", encoding="utf-8")

    parser = CsvParser()
    result = parser.parse(str(csv_path))

    assert result.records == [{"id": "1", "name": "Alice"}]
    assert result.metadata["delimiter"] == ";"


def test_csv_parser_reports_mismatched_columns(tmp_path):
    csv_path = tmp_path / "bad.csv"
    csv_path.write_text("id,name\n1,Alice\n2\n", encoding="utf-8")

    parser = CsvParser()
    result = parser.parse(str(csv_path))

    assert len(result.errors) == 1
    assert result.errors[0].row == 3
    assert "mismatched" in result.errors[0].message.lower()
```

**Step 2: Run tests to verify they fail**

Run: `pytest DataGuard/tests/unit/parser/test_csv_parser.py::test_csv_parser_detects_semicolon_delimiter DataGuard/tests/unit/parser/test_csv_parser.py::test_csv_parser_reports_mismatched_columns -v`
Expected: FAIL with missing behavior

**Step 3: Implement minimal behavior**

```python
# DataGuard/src/dataguard/parser/csv_parser.py
from .base import BaseParser, ParseResult, ParseErrorItem


class CsvParser(BaseParser):
    def parse(self, file_path: str, encoding: str | None = None) -> ParseResult:
        used_encoding = encoding or "utf-8"
        errors: list[ParseErrorItem] = []
        with open(file_path, "r", encoding=used_encoding, newline="") as handle:
            sample = handle.read(1024)
            handle.seek(0)
            dialect = csv.Sniffer().sniff(sample) if sample else csv.excel
            reader = csv.reader(handle, dialect=dialect)
            rows = list(reader)

        if not rows:
            return ParseResult(records=[], errors=[], metadata={"delimiter": dialect.delimiter})

        header = rows[0]
        records: list[dict[str, str]] = []
        for index, row in enumerate(rows[1:], start=2):
            if len(row) != len(header):
                errors.append(ParseErrorItem(row=index, message="Mismatched column count"))
                continue
            records.append(dict(zip(header, row)))

        return ParseResult(records=records, errors=errors, metadata={"delimiter": dialect.delimiter})
```

**Step 4: Run tests to verify they pass**

Run: `pytest DataGuard/tests/unit/parser/test_csv_parser.py::test_csv_parser_detects_semicolon_delimiter DataGuard/tests/unit/parser/test_csv_parser.py::test_csv_parser_reports_mismatched_columns -v`
Expected: PASS

**Step 5: Commit**

```bash
git add DataGuard/src/dataguard/parser/csv_parser.py DataGuard/tests/unit/parser/test_csv_parser.py
git commit -m "feat: detect delimiter and report mismatched columns"
```

---

### Task 4: JSON / JSONL parser

**Files:**
- Create: `DataGuard/src/dataguard/parser/json_parser.py`
- Create: `DataGuard/tests/unit/parser/test_json_parser.py`

**Step 1: Write failing tests**

```python
def test_json_parser_reads_array(tmp_path):
    json_path = tmp_path / "data.json"
    json_path.write_text('[{"id": 1}, {"id": 2}]', encoding="utf-8")

    parser = JsonParser()
    result = parser.parse(str(json_path))

    assert result.records == [{"id": 1}, {"id": 2}]
    assert result.errors == []


def test_json_parser_reads_jsonl(tmp_path):
    jsonl_path = tmp_path / "data.jsonl"
    jsonl_path.write_text('{"id": 1}\n{"id": 2}\n', encoding="utf-8")

    parser = JsonParser()
    result = parser.parse(str(jsonl_path))

    assert result.records == [{"id": 1}, {"id": 2}]
```

**Step 2: Run tests to verify they fail**

Run: `pytest DataGuard/tests/unit/parser/test_json_parser.py -v`
Expected: FAIL with ImportError or AttributeError

**Step 3: Write minimal implementation**

```python
# DataGuard/src/dataguard/parser/json_parser.py
import json
from .base import BaseParser, ParseResult, ParseErrorItem


class JsonParser(BaseParser):
    def parse(self, file_path: str, encoding: str | None = None) -> ParseResult:
        used_encoding = encoding or "utf-8"
        errors: list[ParseErrorItem] = []
        records: list[dict] = []

        with open(file_path, "r", encoding=used_encoding) as handle:
            content = handle.read().strip()

        if not content:
            return ParseResult(records=[], errors=[], metadata={})

        if content.lstrip().startswith("{") and "\n" in content:
            for index, line in enumerate(content.splitlines(), start=1):
                if not line.strip():
                    continue
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError as exc:
                    errors.append(ParseErrorItem(row=index, message=str(exc)))
        else:
            data = json.loads(content)
            if isinstance(data, list):
                records = data
            elif isinstance(data, dict):
                records = [data]
            else:
                errors.append(ParseErrorItem(row=1, message="JSON root must be object or array"))

        return ParseResult(records=records, errors=errors, metadata={})
```

**Step 4: Run tests to verify they pass**

Run: `pytest DataGuard/tests/unit/parser/test_json_parser.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add DataGuard/src/dataguard/parser/json_parser.py DataGuard/tests/unit/parser/test_json_parser.py
git commit -m "feat: add JSON and JSONL parsing"
```

---

### Task 5: Encoding detection utility

**Files:**
- Create: `DataGuard/src/dataguard/parser/encoding.py`
- Create: `DataGuard/tests/unit/parser/test_encoding.py`

**Step 1: Write failing test**

```python
def test_detect_encoding_utf8(tmp_path):
    data_path = tmp_path / "utf8.txt"
    data_path.write_bytes("hello".encode("utf-8"))

    encoding = detect_encoding(str(data_path))

    assert encoding.lower() in {"utf-8", "utf_8"}
```

**Step 2: Run test to verify it fails**

Run: `pytest DataGuard/tests/unit/parser/test_encoding.py::test_detect_encoding_utf8 -v`
Expected: FAIL with ImportError or NameError

**Step 3: Implement detect_encoding**

```python
# DataGuard/src/dataguard/parser/encoding.py
import chardet


def detect_encoding(file_path: str) -> str:
    with open(file_path, "rb") as handle:
        raw = handle.read()
    result = chardet.detect(raw)
    encoding = result.get("encoding") or "utf-8"
    return encoding
```

**Step 4: Run test to verify it passes**

Run: `pytest DataGuard/tests/unit/parser/test_encoding.py::test_detect_encoding_utf8 -v`
Expected: PASS

**Step 5: Commit**

```bash
git add DataGuard/src/dataguard/parser/encoding.py DataGuard/tests/unit/parser/test_encoding.py
git commit -m "feat: add encoding detection"
```

---

### Task 6: Parser package exports

**Files:**
- Create: `DataGuard/src/dataguard/parser/__init__.py`

**Step 1: Write failing test (import surface)**

```python
def test_parser_exports():
    from dataguard.parser import CsvParser, JsonParser
    assert CsvParser and JsonParser
```

**Step 2: Run test to verify it fails**

Run: `pytest DataGuard/tests/unit/parser/test_csv_parser.py::test_parser_exports -v`
Expected: FAIL with ImportError

**Step 3: Implement exports**

```python
# DataGuard/src/dataguard/parser/__init__.py
from .csv_parser import CsvParser
from .json_parser import JsonParser
from .encoding import detect_encoding

__all__ = ["CsvParser", "JsonParser", "detect_encoding"]
```

**Step 4: Run test to verify it passes**

Run: `pytest DataGuard/tests/unit/parser/test_csv_parser.py::test_parser_exports -v`
Expected: PASS

**Step 5: Commit**

```bash
git add DataGuard/src/dataguard/parser/__init__.py DataGuard/tests/unit/parser/test_csv_parser.py
git commit -m "feat: export parser utilities"
```

---

### Task 7: Phase 1 test run

**Files:**
- Modify: none
- Test: `DataGuard/tests/unit/parser/`

**Step 1: Run full parser unit tests**

Run: `pytest DataGuard/tests/unit/parser -v`
Expected: PASS

**Step 2: Commit (if needed)**

```bash
git add DataGuard/tests/unit/parser
git commit -m "test: verify parser unit tests"
```
