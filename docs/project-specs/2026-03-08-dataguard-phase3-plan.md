# DataGuard Phase 3 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Implement transformer operations (type cast, date format, fill missing, dedup, field map) with ordered execution and tests.

**Architecture:** Transformer engine applies a list of transforms in YAML order using an operation registry. Each operation is a pure function/class that accepts and returns list[dict] without I/O.

**Tech Stack:** Python 3.10+, pytest

---

### Task 1: Transformer engine skeleton and registry

**Files:**
- Create: `src/dataguard/transformer/engine.py`
- Create: `tests/unit/transformer/test_engine.py`

**Step 1: Write the failing test**

```python
def test_engine_applies_operations_in_order():
    from dataguard.transformer.engine import apply_transforms

    records = [{"age": "1"}, {"age": "2"}]
    transforms = [
        {"operation": "type_cast", "column": "age", "target_type": "integer"},
        {"operation": "dedup", "keys": ["age"], "keep": "first"},
    ]

    result = apply_transforms(records, transforms)

    assert result == [{"age": 1}, {"age": 2}]
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/unit/transformer/test_engine.py::test_engine_applies_operations_in_order -v`
Expected: FAIL with ImportError

**Step 3: Write minimal implementation**

```python
from typing import Any, Callable


Operation = Callable[[list[dict[str, Any]], dict[str, Any]], list[dict[str, Any]]]


def apply_transforms(records: list[dict[str, Any]], transforms: list[dict[str, Any]]):
    from .type_cast import type_cast
    from .dedup import dedup

    registry: dict[str, Operation] = {
        "type_cast": type_cast,
        "dedup": dedup,
    }

    current = records
    for transform in transforms:
        name = transform["operation"]
        handler = registry[name]
        current = handler(current, transform)
    return current
```

**Step 4: Run test to verify it passes**

Run: `uv run pytest tests/unit/transformer/test_engine.py::test_engine_applies_operations_in_order -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/dataguard/transformer/engine.py tests/unit/transformer/test_engine.py
git commit -m "Add transformer engine" -m "Ultraworked with [Sisyphus](https://github.com/code-yeongyu/oh-my-opencode)" -m "Co-authored-by: Sisyphus <clio-agent@sisyphuslabs.ai>"
```

---

### Task 2: Type cast operation

**Files:**
- Create: `src/dataguard/transformer/type_cast.py`
- Test: `tests/unit/transformer/test_type_cast.py`

**Step 1: Write the failing test**

```python
def test_type_cast_integer():
    from dataguard.transformer.type_cast import type_cast

    records = [{"age": "10"}, {"age": "bad"}]
    result = type_cast(records, {"column": "age", "target_type": "integer"})

    assert result[0]["age"] == 10
    assert result[1]["age"] == "bad"
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/unit/transformer/test_type_cast.py::test_type_cast_integer -v`
Expected: FAIL with ImportError

**Step 3: Write minimal implementation**

```python
def type_cast(records, transform):
    column = transform["column"]
    target = transform["target_type"]

    def cast(value):
        if target == "integer":
            return int(value)
        if target == "float":
            return float(value)
        if target == "string":
            return str(value)
        if target == "boolean":
            return str(value).lower() in {"true", "1", "yes"}
        return value

    for record in records:
        if column in record:
            try:
                record[column] = cast(record[column])
            except (ValueError, TypeError):
                pass
    return records
```

**Step 4: Run test to verify it passes**

Run: `uv run pytest tests/unit/transformer/test_type_cast.py::test_type_cast_integer -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/dataguard/transformer/type_cast.py tests/unit/transformer/test_type_cast.py
git commit -m "Add type cast transformer" -m "Ultraworked with [Sisyphus](https://github.com/code-yeongyu/oh-my-opencode)" -m "Co-authored-by: Sisyphus <clio-agent@sisyphuslabs.ai>"
```

---

### Task 3: Date format operation

**Files:**
- Create: `src/dataguard/transformer/date_format.py`
- Test: `tests/unit/transformer/test_date_format.py`

**Step 1: Write the failing test**

```python
def test_date_format_converts():
    from dataguard.transformer.date_format import date_format

    records = [{"join": "2020/01/02"}, {"join": "bad"}]
    transform = {
        "column": "join",
        "source_formats": ["%Y/%m/%d"],
        "target_format": "%Y-%m-%d",
    }

    result = date_format(records, transform)

    assert result[0]["join"] == "2020-01-02"
    assert result[1]["join"] == "bad"
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/unit/transformer/test_date_format.py::test_date_format_converts -v`
Expected: FAIL with ImportError

**Step 3: Write minimal implementation**

```python
from datetime import datetime


def date_format(records, transform):
    column = transform["column"]
    source_formats = transform.get("source_formats", [])
    target = transform["target_format"]

    for record in records:
        if column not in record:
            continue
        value = record[column]
        for fmt in source_formats:
            try:
                parsed = datetime.strptime(value, fmt)
                record[column] = parsed.strftime(target)
                break
            except (ValueError, TypeError):
                continue
    return records
```

**Step 4: Run test to verify it passes**

Run: `uv run pytest tests/unit/transformer/test_date_format.py::test_date_format_converts -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/dataguard/transformer/date_format.py tests/unit/transformer/test_date_format.py
git commit -m "Add date format transformer" -m "Ultraworked with [Sisyphus](https://github.com/code-yeongyu/oh-my-opencode)" -m "Co-authored-by: Sisyphus <clio-agent@sisyphuslabs.ai>"
```

---

### Task 4: Fill missing operation

**Files:**
- Create: `src/dataguard/transformer/fill_missing.py`
- Test: `tests/unit/transformer/test_fill_missing.py`

**Step 1: Write the failing test**

```python
def test_fill_missing_default():
    from dataguard.transformer.fill_missing import fill_missing

    records = [{"x": None}, {"x": 5}]
    transform = {"column": "x", "strategy": "default", "value": 0}

    result = fill_missing(records, transform)

    assert result[0]["x"] == 0
    assert result[1]["x"] == 5
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/unit/transformer/test_fill_missing.py::test_fill_missing_default -v`
Expected: FAIL with ImportError

**Step 3: Write minimal implementation**

```python
def fill_missing(records, transform):
    column = transform["column"]
    strategy = transform["strategy"]

    if strategy == "default":
        value = transform.get("value")
        for record in records:
            if record.get(column) in (None, ""):
                record[column] = value
        return records

    if strategy == "drop_row":
        return [r for r in records if r.get(column) not in (None, "")]

    if strategy == "forward_fill":
        last_value = None
        for record in records:
            if record.get(column) not in (None, ""):
                last_value = record[column]
            elif last_value is not None:
                record[column] = last_value
        return records

    if strategy == "mean":
        values = [r.get(column) for r in records if isinstance(r.get(column), (int, float))]
        if values:
            mean_value = sum(values) / len(values)
            for record in records:
                if record.get(column) in (None, ""):
                    record[column] = mean_value
        return records

    return records
```

**Step 4: Run test to verify it passes**

Run: `uv run pytest tests/unit/transformer/test_fill_missing.py::test_fill_missing_default -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/dataguard/transformer/fill_missing.py tests/unit/transformer/test_fill_missing.py
git commit -m "Add fill missing transformer" -m "Ultraworked with [Sisyphus](https://github.com/code-yeongyu/oh-my-opencode)" -m "Co-authored-by: Sisyphus <clio-agent@sisyphuslabs.ai>"
```

---

### Task 5: Dedup operation

**Files:**
- Create: `src/dataguard/transformer/dedup.py`
- Test: `tests/unit/transformer/test_dedup.py`

**Step 1: Write the failing test**

```python
def test_dedup_keep_first():
    from dataguard.transformer.dedup import dedup

    records = [{"id": 1}, {"id": 1}, {"id": 2}]
    transform = {"keys": ["id"], "keep": "first"}

    result = dedup(records, transform)

    assert result == [{"id": 1}, {"id": 2}]
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/unit/transformer/test_dedup.py::test_dedup_keep_first -v`
Expected: FAIL with ImportError

**Step 3: Write minimal implementation**

```python
def dedup(records, transform):
    keys = transform["keys"]
    keep = transform.get("keep", "first")

    seen = {}
    order = []
    for index, record in enumerate(records):
        key = tuple(record.get(k) for k in keys)
        if key not in seen:
            seen[key] = []
        seen[key].append(index)
        order.append(key)

    if keep == "none":
        return [r for i, r in enumerate(records) if len(seen[order[i]]) == 1]
    if keep == "last":
        keep_indexes = {indexes[-1] for indexes in seen.values()}
        return [r for i, r in enumerate(records) if i in keep_indexes]

    keep_indexes = {indexes[0] for indexes in seen.values()}
    return [r for i, r in enumerate(records) if i in keep_indexes]
```

**Step 4: Run test to verify it passes**

Run: `uv run pytest tests/unit/transformer/test_dedup.py::test_dedup_keep_first -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/dataguard/transformer/dedup.py tests/unit/transformer/test_dedup.py
git commit -m "Add dedup transformer" -m "Ultraworked with [Sisyphus](https://github.com/code-yeongyu/oh-my-opencode)" -m "Co-authored-by: Sisyphus <clio-agent@sisyphuslabs.ai>"
```

---

### Task 6: Field map operation

**Files:**
- Create: `src/dataguard/transformer/field_map.py`
- Test: `tests/unit/transformer/test_field_map.py`

**Step 1: Write the failing test**

```python
def test_field_map_rename_and_drop():
    from dataguard.transformer.field_map import field_map

    records = [{"id": 1, "temp": "x"}]
    transform = {"rename": {"id": "ID"}, "drop": ["temp"]}

    result = field_map(records, transform)

    assert result == [{"ID": 1}]
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/unit/transformer/test_field_map.py::test_field_map_rename_and_drop -v`
Expected: FAIL with ImportError

**Step 3: Write minimal implementation**

```python
def field_map(records, transform):
    rename = transform.get("rename", {})
    drop = set(transform.get("drop", []))

    for record in records:
        for source, target in rename.items():
            if source in record:
                record[target] = record.pop(source)
        for key in drop:
            record.pop(key, None)
    return records
```

**Step 4: Run test to verify it passes**

Run: `uv run pytest tests/unit/transformer/test_field_map.py::test_field_map_rename_and_drop -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/dataguard/transformer/field_map.py tests/unit/transformer/test_field_map.py
git commit -m "Add field map transformer" -m "Ultraworked with [Sisyphus](https://github.com/code-yeongyu/oh-my-opencode)" -m "Co-authored-by: Sisyphus <clio-agent@sisyphuslabs.ai>"
```

---

### Task 7: Phase 3 unit test run

**Files:**
- Modify: none
- Test: `tests/unit/transformer/`

**Step 1: Run transformer unit tests**

Run: `uv run pytest tests/unit/transformer -v`
Expected: PASS

**Step 2: Commit (if needed)**

```bash
git add tests/unit/transformer
git commit -m "Test transformer operations" -m "Ultraworked with [Sisyphus](https://github.com/code-yeongyu/oh-my-opencode)" -m "Co-authored-by: Sisyphus <clio-agent@sisyphuslabs.ai>"
```
