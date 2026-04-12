# DataGuard Phase 2 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Implement schema loading and validation engine with core validators and tests.

**Architecture:** Add schema models and loader to parse YAML schema into dataclasses. Implement validators for string, numeric, date, enum, boolean, and a validation engine that iterates records and returns `ValidationResult` entries.

**Tech Stack:** Python 3.10+, PyYAML, pytest

---

### Task 1: Schema data models

**Files:**
- Create: `src/dataguard/schema/models.py`
- Test: `tests/unit/schema/test_models.py`

**Step 1: Write the failing test**

```python
def test_schema_models_default_values():
    from dataguard.schema.models import Schema, ColumnSchema

    column = ColumnSchema(name="age", type="integer", required=True)
    schema = Schema(name="employees", version="1.0", strict=True, columns=[column])

    assert schema.name == "employees"
    assert schema.strict is True
    assert schema.columns[0].name == "age"
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/unit/schema/test_models.py::test_schema_models_default_values -v`
Expected: FAIL with ImportError or AttributeError

**Step 3: Write minimal implementation**

```python
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
    case_sensitive: bool = True
    decimal_places: int | None = None
    true_values: list[str] | None = None
    false_values: list[str] | None = None


@dataclass
class Schema:
    name: str
    version: str
    strict: bool = True
    columns: list[ColumnSchema] = field(default_factory=list)
```

**Step 4: Run test to verify it passes**

Run: `uv run pytest tests/unit/schema/test_models.py::test_schema_models_default_values -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/dataguard/schema/models.py tests/unit/schema/test_models.py
git commit -m "Add schema models" -m "Ultraworked with [Sisyphus](https://github.com/code-yeongyu/oh-my-opencode)" -m "Co-authored-by: Sisyphus <clio-agent@sisyphuslabs.ai>"
```

---

### Task 2: Schema loader (YAML)

**Files:**
- Create: `src/dataguard/schema/loader.py`
- Modify: `src/dataguard/schema/__init__.py`
- Test: `tests/unit/schema/test_loader.py`

**Step 1: Write the failing test**

```python
def test_loader_parses_schema(tmp_path):
    from dataguard.schema.loader import load_schema

    schema_path = tmp_path / "schema.yaml"
    schema_path.write_text(
        """
schema:
  name: "employees"
  version: "1.0"
  strict: true
  columns:
    - name: "age"
      type: "integer"
      required: true
      min: 18
      max: 65
""",
        encoding="utf-8",
    )

    schema = load_schema(str(schema_path))

    assert schema.name == "employees"
    assert schema.columns[0].name == "age"
    assert schema.columns[0].min == 18
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/unit/schema/test_loader.py::test_loader_parses_schema -v`
Expected: FAIL with ImportError or AttributeError

**Step 3: Write minimal implementation**

```python
import yaml
from .models import Schema, ColumnSchema


def load_schema(file_path: str) -> Schema:
    with open(file_path, "r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}

    raw = data.get("schema", {})
    columns = [ColumnSchema(**col) for col in raw.get("columns", [])]
    return Schema(
        name=raw.get("name", ""),
        version=raw.get("version", ""),
        strict=bool(raw.get("strict", True)),
        columns=columns,
    )
```

```python
# src/dataguard/schema/__init__.py
from .loader import load_schema
from .models import Schema, ColumnSchema

__all__ = ["load_schema", "Schema", "ColumnSchema"]
```

**Step 4: Run test to verify it passes**

Run: `uv run pytest tests/unit/schema/test_loader.py::test_loader_parses_schema -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/dataguard/schema/loader.py src/dataguard/schema/__init__.py tests/unit/schema/test_loader.py
git commit -m "Add schema loader" -m "Ultraworked with [Sisyphus](https://github.com/code-yeongyu/oh-my-opencode)" -m "Co-authored-by: Sisyphus <clio-agent@sisyphuslabs.ai>"
```

---

### Task 3: Validation result model

**Files:**
- Create: `src/dataguard/schema/engine.py`
- Test: `tests/unit/schema/test_engine.py`

**Step 1: Write the failing test**

```python
def test_validation_result_fields():
    from dataguard.schema.engine import ValidationResult

    result = ValidationResult(row=1, column="age", value=20, level="PASS", code="OK", message="")

    assert result.row == 1
    assert result.column == "age"
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/unit/schema/test_engine.py::test_validation_result_fields -v`
Expected: FAIL with ImportError

**Step 3: Write minimal implementation**

```python
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
```

**Step 4: Run test to verify it passes**

Run: `uv run pytest tests/unit/schema/test_engine.py::test_validation_result_fields -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/dataguard/schema/engine.py tests/unit/schema/test_engine.py
git commit -m "Add validation result model" -m "Ultraworked with [Sisyphus](https://github.com/code-yeongyu/oh-my-opencode)" -m "Co-authored-by: Sisyphus <clio-agent@sisyphuslabs.ai>"
```

---

### Task 4: String validator

**Files:**
- Create: `src/dataguard/schema/validators/base.py`
- Create: `src/dataguard/schema/validators/string.py`
- Test: `tests/unit/schema/validators/test_string.py`

**Step 1: Write the failing test**

```python
def test_string_validator_length_and_pattern():
    from dataguard.schema.validators.string import StringValidator
    from dataguard.schema.models import ColumnSchema

    schema = ColumnSchema(name="email", type="string", required=True, max_length=10, pattern="^a")
    validator = StringValidator(schema)

    assert validator.validate("abc").code == "OK"
    assert validator.validate("toolongvalue").code == "LENGTH_ERROR"
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/unit/schema/validators/test_string.py::test_string_validator_length_and_pattern -v`
Expected: FAIL with ImportError

**Step 3: Write minimal implementation**

```python
from dataclasses import dataclass
import re
from .base import BaseValidator, ValidationMessage


@dataclass
class ValidationMessage:
    code: str
    message: str


class StringValidator(BaseValidator):
    def validate(self, value: str) -> ValidationMessage:
        if self.schema.max_length is not None and len(value) > self.schema.max_length:
            return ValidationMessage(code="LENGTH_ERROR", message="Too long")
        if self.schema.pattern and not re.match(self.schema.pattern, value):
            return ValidationMessage(code="PATTERN_ERROR", message="Pattern mismatch")
        return ValidationMessage(code="OK", message="")
```

```python
# src/dataguard/schema/validators/base.py
class BaseValidator:
    def __init__(self, schema):
        self.schema = schema
```

**Step 4: Run test to verify it passes**

Run: `uv run pytest tests/unit/schema/validators/test_string.py::test_string_validator_length_and_pattern -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/dataguard/schema/validators/base.py src/dataguard/schema/validators/string.py tests/unit/schema/validators/test_string.py
git commit -m "Add string validator" -m "Ultraworked with [Sisyphus](https://github.com/code-yeongyu/oh-my-opencode)" -m "Co-authored-by: Sisyphus <clio-agent@sisyphuslabs.ai>"
```

---

### Task 5: Integer and float validators

**Files:**
- Create: `src/dataguard/schema/validators/numeric.py`
- Test: `tests/unit/schema/validators/test_numeric.py`

**Step 1: Write the failing test**

```python
def test_numeric_validator_range():
    from dataguard.schema.validators.numeric import IntegerValidator
    from dataguard.schema.models import ColumnSchema

    schema = ColumnSchema(name="age", type="integer", min=18, max=65)
    validator = IntegerValidator(schema)

    assert validator.validate(20).code == "OK"
    assert validator.validate(10).code == "OUT_OF_RANGE"
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/unit/schema/validators/test_numeric.py::test_numeric_validator_range -v`
Expected: FAIL with ImportError

**Step 3: Write minimal implementation**

```python
from .base import BaseValidator, ValidationMessage


class NumericValidator(BaseValidator):
    def _range_check(self, value: float) -> ValidationMessage:
        if self.schema.min is not None and value < self.schema.min:
            return ValidationMessage(code="OUT_OF_RANGE", message="Below min")
        if self.schema.max is not None and value > self.schema.max:
            return ValidationMessage(code="OUT_OF_RANGE", message="Above max")
        return ValidationMessage(code="OK", message="")


class IntegerValidator(NumericValidator):
    def validate(self, value: int) -> ValidationMessage:
        return self._range_check(value)


class FloatValidator(NumericValidator):
    def validate(self, value: float) -> ValidationMessage:
        return self._range_check(value)
```

**Step 4: Run test to verify it passes**

Run: `uv run pytest tests/unit/schema/validators/test_numeric.py::test_numeric_validator_range -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/dataguard/schema/validators/numeric.py tests/unit/schema/validators/test_numeric.py
git commit -m "Add numeric validators" -m "Ultraworked with [Sisyphus](https://github.com/code-yeongyu/oh-my-opencode)" -m "Co-authored-by: Sisyphus <clio-agent@sisyphuslabs.ai>"
```

---

### Task 6: Date validator

**Files:**
- Create: `src/dataguard/schema/validators/date.py`
- Test: `tests/unit/schema/validators/test_date.py`

**Step 1: Write the failing test**

```python
def test_date_validator_format_and_range():
    from dataguard.schema.validators.date import DateValidator
    from dataguard.schema.models import ColumnSchema

    schema = ColumnSchema(name="join_date", type="date", format="%Y-%m-%d", min="2020-01-01")
    validator = DateValidator(schema)

    assert validator.validate("2021-01-01").code == "OK"
    assert validator.validate("2019-12-31").code == "OUT_OF_RANGE"
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/unit/schema/validators/test_date.py::test_date_validator_format_and_range -v`
Expected: FAIL with ImportError

**Step 3: Write minimal implementation**

```python
from datetime import datetime
from .base import BaseValidator, ValidationMessage


class DateValidator(BaseValidator):
    def validate(self, value: str) -> ValidationMessage:
        try:
            parsed = datetime.strptime(value, self.schema.format or "%Y-%m-%d")
        except ValueError:
            return ValidationMessage(code="FORMAT_ERROR", message="Invalid date format")

        if self.schema.min:
            min_date = datetime.strptime(self.schema.min, self.schema.format or "%Y-%m-%d")
            if parsed < min_date:
                return ValidationMessage(code="OUT_OF_RANGE", message="Below min")
        if self.schema.max:
            max_date = datetime.strptime(self.schema.max, self.schema.format or "%Y-%m-%d")
            if parsed > max_date:
                return ValidationMessage(code="OUT_OF_RANGE", message="Above max")

        return ValidationMessage(code="OK", message="")
```

**Step 4: Run test to verify it passes**

Run: `uv run pytest tests/unit/schema/validators/test_date.py::test_date_validator_format_and_range -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/dataguard/schema/validators/date.py tests/unit/schema/validators/test_date.py
git commit -m "Add date validator" -m "Ultraworked with [Sisyphus](https://github.com/code-yeongyu/oh-my-opencode)" -m "Co-authored-by: Sisyphus <clio-agent@sisyphuslabs.ai>"
```

---

### Task 7: Enum and boolean validators

**Files:**
- Create: `src/dataguard/schema/validators/enum.py`
- Create: `src/dataguard/schema/validators/boolean.py`
- Test: `tests/unit/schema/validators/test_enum.py`
- Test: `tests/unit/schema/validators/test_boolean.py`

**Step 1: Write the failing tests**

```python
def test_enum_validator_values():
    from dataguard.schema.validators.enum import EnumValidator
    from dataguard.schema.models import ColumnSchema

    schema = ColumnSchema(name="dept", type="enum", values=["HR", "ENG"], case_sensitive=False)
    validator = EnumValidator(schema)

    assert validator.validate("hr").code == "OK"
    assert validator.validate("sales").code == "NOT_IN_ENUM"
```

```python
def test_boolean_validator_values():
    from dataguard.schema.validators.boolean import BooleanValidator
    from dataguard.schema.models import ColumnSchema

    schema = ColumnSchema(name="active", type="boolean", true_values=["yes"], false_values=["no"])
    validator = BooleanValidator(schema)

    assert validator.validate("yes").code == "OK"
    assert validator.validate("maybe").code == "INVALID_BOOLEAN"
```

**Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/unit/schema/validators/test_enum.py::test_enum_validator_values -v`
Expected: FAIL with ImportError

Run: `uv run pytest tests/unit/schema/validators/test_boolean.py::test_boolean_validator_values -v`
Expected: FAIL with ImportError

**Step 3: Write minimal implementation**

```python
from .base import BaseValidator, ValidationMessage


class EnumValidator(BaseValidator):
    def validate(self, value: str) -> ValidationMessage:
        values = self.schema.values or []
        if not self.schema.case_sensitive:
            values = [str(v).lower() for v in values]
            if str(value).lower() not in values:
                return ValidationMessage(code="NOT_IN_ENUM", message="Invalid enum")
        else:
            if value not in values:
                return ValidationMessage(code="NOT_IN_ENUM", message="Invalid enum")
        return ValidationMessage(code="OK", message="")
```

```python
from .base import BaseValidator, ValidationMessage


class BooleanValidator(BaseValidator):
    def validate(self, value: str) -> ValidationMessage:
        true_values = self.schema.true_values or ["true", "1", "yes"]
        false_values = self.schema.false_values or ["false", "0", "no"]
        if value in true_values or value in false_values:
            return ValidationMessage(code="OK", message="")
        return ValidationMessage(code="INVALID_BOOLEAN", message="Invalid boolean")
```

**Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/unit/schema/validators/test_enum.py::test_enum_validator_values -v`
Expected: PASS

Run: `uv run pytest tests/unit/schema/validators/test_boolean.py::test_boolean_validator_values -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/dataguard/schema/validators/enum.py src/dataguard/schema/validators/boolean.py tests/unit/schema/validators/test_enum.py tests/unit/schema/validators/test_boolean.py
git commit -m "Add enum and boolean validators" -m "Ultraworked with [Sisyphus](https://github.com/code-yeongyu/oh-my-opencode)" -m "Co-authored-by: Sisyphus <clio-agent@sisyphuslabs.ai>"
```

---

### Task 8: Validation engine

**Files:**
- Modify: `src/dataguard/schema/engine.py`
- Create: `tests/unit/schema/test_engine_validate.py`

**Step 1: Write the failing test**

```python
def test_engine_validates_required_field():
    from dataguard.schema.engine import validate_records
    from dataguard.schema.models import Schema, ColumnSchema

    schema = Schema(
        name="employees",
        version="1.0",
        strict=True,
        columns=[ColumnSchema(name="age", type="integer", required=True)],
    )

    results = validate_records(schema, [{"age": 20}, {}])

    assert results[0].level == "PASS"
    assert results[1].level == "ERROR"
    assert results[1].code == "REQUIRED_MISSING"
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/unit/schema/test_engine_validate.py::test_engine_validates_required_field -v`
Expected: FAIL with ImportError or AttributeError

**Step 3: Write minimal implementation**

```python
from typing import Any
from .models import Schema


def validate_records(schema: Schema, records: list[dict[str, Any]]):
    results = []
    for row_index, record in enumerate(records, start=1):
        for column in schema.columns:
            if column.required and column.name not in record:
                results.append(
                    ValidationResult(
                        row=row_index,
                        column=column.name,
                        value=None,
                        level="ERROR",
                        code="REQUIRED_MISSING",
                        message="Required field missing",
                    )
                )
            else:
                results.append(
                    ValidationResult(
                        row=row_index,
                        column=column.name,
                        value=record.get(column.name),
                        level="PASS",
                        code="OK",
                        message="",
                    )
                )
    return results
```

**Step 4: Run test to verify it passes**

Run: `uv run pytest tests/unit/schema/test_engine_validate.py::test_engine_validates_required_field -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/dataguard/schema/engine.py tests/unit/schema/test_engine_validate.py
git commit -m "Add validation engine" -m "Ultraworked with [Sisyphus](https://github.com/code-yeongyu/oh-my-opencode)" -m "Co-authored-by: Sisyphus <clio-agent@sisyphuslabs.ai>"
```

---

### Task 9: Phase 2 unit test run

**Files:**
- Modify: none
- Test: `tests/unit/schema/`

**Step 1: Run schema unit tests**

Run: `uv run pytest tests/unit/schema -v`
Expected: PASS

**Step 2: Commit (if needed)**

```bash
git add tests/unit/schema
git commit -m "Test schema validators" -m "Ultraworked with [Sisyphus](https://github.com/code-yeongyu/oh-my-opencode)" -m "Co-authored-by: Sisyphus <clio-agent@sisyphuslabs.ai>"
```
