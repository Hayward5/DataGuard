# Week 9 Transformer Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first usable `transformer` foundation for DataGuard with ordered transform execution, `type_cast`, `fill_missing` (`default`, `drop_row`), `dedup` (`keep=first`, `keep=last`), and minimal integration coverage.

**Architecture:** Add a pure `transformer` module under `src/dataguard/transformer/` that accepts `list[dict]` records plus a `transforms` array and returns transformed records with no file I/O. Keep Week 9 scoped to core transformation logic and tests only; do not connect it to `clean` or `convert` CLI flows yet.

**Tech Stack:** Python 3.12, pytest, existing `src/` package layout, TDD, small `test -> feat` commits.

---

### Task 1: Transformer Package Skeleton and Ordered Engine

**Files:**
- Create: `src/dataguard/transformer/__init__.py`
- Create: `src/dataguard/transformer/engine.py`
- Test: `tests/unit/transformer/test_engine.py`

- [ ] **Step 1: Write the failing test**

```python
def test_engine_applies_registered_operations_in_order():
    from dataguard.transformer.engine import apply_transforms

    records = [{"age": "1"}, {"age": "2"}]
    transforms = [
        {"operation": "type_cast", "column": "age", "target_type": "integer"},
        {"operation": "dedup", "keys": ["age"], "keep": "first"},
    ]

    result = apply_transforms(records, transforms)

    assert result == [{"age": 1}, {"age": 2}]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/unit/transformer/test_engine.py -q`
Expected: FAIL with import error for `dataguard.transformer.engine`

- [ ] **Step 3: Write minimal implementation**

```python
# src/dataguard/transformer/__init__.py
from dataguard.transformer.engine import apply_transforms

__all__ = ["apply_transforms"]
```

```python
# src/dataguard/transformer/engine.py
from typing import Any, Callable

Operation = Callable[[list[dict[str, Any]], dict[str, Any]], list[dict[str, Any]]]


def apply_transforms(records: list[dict[str, Any]], transforms: list[dict[str, Any]]):
    from dataguard.transformer.dedup import dedup
    from dataguard.transformer.fill_missing import fill_missing
    from dataguard.transformer.type_cast import type_cast

    registry: dict[str, Operation] = {
        "type_cast": type_cast,
        "fill_missing": fill_missing,
        "dedup": dedup,
    }

    current = [dict(record) for record in records]
    for transform in transforms:
        name = transform["operation"]
        if name not in registry:
            raise ValueError(f"Unsupported transform operation: {name}")
        current = registry[name](current, transform)
    return current
```

- [ ] **Step 4: Run test to verify it passes**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/unit/transformer/test_engine.py -q`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/dataguard/transformer/__init__.py src/dataguard/transformer/engine.py tests/unit/transformer/test_engine.py
git commit -m "feat: add transformer engine foundation"
```

---

### Task 2: Type Cast Operation

**Files:**
- Create: `src/dataguard/transformer/type_cast.py`
- Test: `tests/unit/transformer/test_type_cast.py`

- [ ] **Step 1: Write the failing tests**

```python
import pytest


@pytest.mark.parametrize(
    ("value", "target_type", "expected"),
    [
        ("10", "integer", 10),
        ("3.5", "float", 3.5),
        (10, "string", "10"),
        ("yes", "boolean", True),
        ("0", "boolean", False),
    ],
)
def test_type_cast_converts_supported_types(value, target_type, expected):
    from dataguard.transformer.type_cast import type_cast

    records = [{"value": value}]
    result = type_cast(records, {"column": "value", "target_type": target_type})

    assert result[0]["value"] == expected


def test_type_cast_keeps_original_value_when_conversion_fails():
    from dataguard.transformer.type_cast import type_cast

    records = [{"value": "bad"}]
    result = type_cast(records, {"column": "value", "target_type": "integer"})

    assert result[0]["value"] == "bad"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/unit/transformer/test_type_cast.py -q`
Expected: FAIL with import error

- [ ] **Step 3: Write minimal implementation**

```python
# src/dataguard/transformer/type_cast.py
def type_cast(records, transform):
    column = transform["column"]
    target_type = transform["target_type"]

    def cast(value):
        if target_type == "integer":
            return int(value)
        if target_type == "float":
            return float(value)
        if target_type == "string":
            return str(value)
        if target_type == "boolean":
            lowered = str(value).strip().lower()
            if lowered in {"true", "1", "yes", "y"}:
                return True
            if lowered in {"false", "0", "no", "n"}:
                return False
            raise ValueError("invalid boolean")
        raise ValueError(f"Unsupported cast target: {target_type}")

    current = [dict(record) for record in records]
    for record in current:
        if column not in record:
            continue
        try:
            record[column] = cast(record[column])
        except (TypeError, ValueError):
            pass
    return current
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/unit/transformer/test_type_cast.py -q`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/dataguard/transformer/type_cast.py tests/unit/transformer/test_type_cast.py
git commit -m "feat: add type cast transformer"
```

---

### Task 3: Fill Missing Default Strategy

**Files:**
- Create: `src/dataguard/transformer/fill_missing.py`
- Test: `tests/unit/transformer/test_fill_missing.py`

- [ ] **Step 1: Write the failing test**

```python
def test_fill_missing_default_replaces_none_and_empty_values():
    from dataguard.transformer.fill_missing import fill_missing

    records = [{"age": None}, {"age": ""}, {"age": 20}]
    result = fill_missing(
        records,
        {"column": "age", "strategy": "default", "value": 0},
    )

    assert result == [{"age": 0}, {"age": 0}, {"age": 20}]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/unit/transformer/test_fill_missing.py::test_fill_missing_default_replaces_none_and_empty_values -q`
Expected: FAIL with import error

- [ ] **Step 3: Write minimal implementation**

```python
# src/dataguard/transformer/fill_missing.py
def fill_missing(records, transform):
    column = transform["column"]
    strategy = transform["strategy"]

    current = [dict(record) for record in records]

    if strategy == "default":
        default_value = transform.get("value")
        for record in current:
            if record.get(column) in (None, ""):
                record[column] = default_value
        return current

    raise ValueError(f"Unsupported fill_missing strategy: {strategy}")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/unit/transformer/test_fill_missing.py::test_fill_missing_default_replaces_none_and_empty_values -q`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/dataguard/transformer/fill_missing.py tests/unit/transformer/test_fill_missing.py
git commit -m "feat: add fill missing default strategy"
```

---

### Task 4: Fill Missing Drop Row Strategy

**Files:**
- Modify: `src/dataguard/transformer/fill_missing.py`
- Modify: `tests/unit/transformer/test_fill_missing.py`

- [ ] **Step 1: Write the failing test**

```python
def test_fill_missing_drop_row_removes_records_with_missing_values():
    from dataguard.transformer.fill_missing import fill_missing

    records = [{"age": None}, {"age": ""}, {"age": 20}]
    result = fill_missing(
        records,
        {"column": "age", "strategy": "drop_row"},
    )

    assert result == [{"age": 20}]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/unit/transformer/test_fill_missing.py::test_fill_missing_drop_row_removes_records_with_missing_values -q`
Expected: FAIL with unsupported strategy

- [ ] **Step 3: Extend minimal implementation**

```python
    if strategy == "drop_row":
        return [record for record in current if record.get(column) not in (None, "")]
```

- [ ] **Step 4: Run fill-missing tests**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/unit/transformer/test_fill_missing.py -q`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/dataguard/transformer/fill_missing.py tests/unit/transformer/test_fill_missing.py
git commit -m "feat: add fill missing drop-row strategy"
```

---

### Task 5: Dedup Keep First Strategy

**Files:**
- Create: `src/dataguard/transformer/dedup.py`
- Test: `tests/unit/transformer/test_dedup.py`

- [ ] **Step 1: Write the failing test**

```python
def test_dedup_keep_first_removes_later_duplicates():
    from dataguard.transformer.dedup import dedup

    records = [
        {"employee_id": "EMP-001", "age": 20},
        {"employee_id": "EMP-001", "age": 21},
        {"employee_id": "EMP-002", "age": 30},
    ]

    result = dedup(records, {"keys": ["employee_id"], "keep": "first"})

    assert result == [
        {"employee_id": "EMP-001", "age": 20},
        {"employee_id": "EMP-002", "age": 30},
    ]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/unit/transformer/test_dedup.py::test_dedup_keep_first_removes_later_duplicates -q`
Expected: FAIL with import error

- [ ] **Step 3: Write minimal implementation**

```python
# src/dataguard/transformer/dedup.py
def dedup(records, transform):
    keys = transform["keys"]
    keep = transform.get("keep", "first")

    if keep != "first":
        raise ValueError(f"Unsupported dedup keep mode: {keep}")

    seen = set()
    result = []
    for record in records:
        key = tuple(record.get(field) for field in keys)
        if key in seen:
            continue
        seen.add(key)
        result.append(dict(record))
    return result
```

- [ ] **Step 4: Run test to verify it passes**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/unit/transformer/test_dedup.py::test_dedup_keep_first_removes_later_duplicates -q`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/dataguard/transformer/dedup.py tests/unit/transformer/test_dedup.py
git commit -m "feat: add dedup keep-first strategy"
```

---

### Task 6: Dedup Keep Last Strategy

**Files:**
- Modify: `src/dataguard/transformer/dedup.py`
- Modify: `tests/unit/transformer/test_dedup.py`

- [ ] **Step 1: Write the failing test**

```python
def test_dedup_keep_last_preserves_latest_duplicate():
    from dataguard.transformer.dedup import dedup

    records = [
        {"employee_id": "EMP-001", "age": 20},
        {"employee_id": "EMP-001", "age": 21},
        {"employee_id": "EMP-002", "age": 30},
    ]

    result = dedup(records, {"keys": ["employee_id"], "keep": "last"})

    assert result == [
        {"employee_id": "EMP-001", "age": 21},
        {"employee_id": "EMP-002", "age": 30},
    ]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/unit/transformer/test_dedup.py::test_dedup_keep_last_preserves_latest_duplicate -q`
Expected: FAIL with unsupported keep mode

- [ ] **Step 3: Extend minimal implementation**

```python
    if keep == "last":
        latest = {}
        order = []
        for record in records:
            key = tuple(record.get(field) for field in keys)
            if key not in latest:
                order.append(key)
            latest[key] = dict(record)
        return [latest[key] for key in order]
```

Full implementation after Task 6:

```python
def dedup(records, transform):
    keys = transform["keys"]
    keep = transform.get("keep", "first")

    if keep == "first":
        seen = set()
        result = []
        for record in records:
            key = tuple(record.get(field) for field in keys)
            if key in seen:
                continue
            seen.add(key)
            result.append(dict(record))
        return result

    if keep == "last":
        latest = {}
        order = []
        for record in records:
            key = tuple(record.get(field) for field in keys)
            if key not in latest:
                order.append(key)
            latest[key] = dict(record)
        return [latest[key] for key in order]

    raise ValueError(f"Unsupported dedup keep mode: {keep}")
```

- [ ] **Step 4: Run dedup tests**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/unit/transformer/test_dedup.py -q`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/dataguard/transformer/dedup.py tests/unit/transformer/test_dedup.py
git commit -m "feat: add dedup keep-last strategy"
```

---

### Task 7: Ordered Integration Coverage for Transformer Foundation

**Files:**
- Create: `tests/integration/test_transformer_flow.py`

- [ ] **Step 1: Write the failing integration tests**

```python
def test_transformer_flow_applies_type_cast_fill_missing_and_dedup():
    from dataguard.transformer.engine import apply_transforms

    records = [
        {"employee_id": "EMP-001", "age": "20", "salary": ""},
        {"employee_id": "EMP-001", "age": "21", "salary": "100"},
        {"employee_id": "EMP-002", "age": "30", "salary": None},
    ]
    transforms = [
        {"operation": "type_cast", "column": "age", "target_type": "integer"},
        {"operation": "fill_missing", "column": "salary", "strategy": "default", "value": "0"},
        {"operation": "dedup", "keys": ["employee_id"], "keep": "last"},
    ]

    result = apply_transforms(records, transforms)

    assert result == [
        {"employee_id": "EMP-001", "age": 21, "salary": "100"},
        {"employee_id": "EMP-002", "age": 30, "salary": "0"},
    ]


def test_transformer_flow_rejects_unknown_operation():
    import pytest
    from dataguard.transformer.engine import apply_transforms

    with pytest.raises(ValueError, match="Unsupported transform operation"):
        apply_transforms([{"x": 1}], [{"operation": "unknown"}])
```

- [ ] **Step 2: Run integration tests to verify they fail**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/integration/test_transformer_flow.py -q`
Expected: FAIL until all operation modules exist and are wired

- [ ] **Step 3: Adjust engine and operations only if needed**

Expected minimal changes:
- `engine.py` already registers all three operations
- no CLI changes
- no parser/schema changes

- [ ] **Step 4: Run transformer-focused suite**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/unit/transformer tests/integration/test_transformer_flow.py -q`
Expected: PASS

- [ ] **Step 5: Run full regression suite**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest -q`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add tests/integration/test_transformer_flow.py src/dataguard/transformer/engine.py src/dataguard/transformer/type_cast.py src/dataguard/transformer/fill_missing.py src/dataguard/transformer/dedup.py tests/unit/transformer
git commit -m "test: add transformer foundation integration coverage"
```

---

### Task 8: Optional Lightweight Documentation Update

**Files:**
- Modify: `docs/week8_progress_report_draft.md` (only if you want to note handoff into week9 later)
- Optional: `docs/plan/week09-transformer-foundation-plan.md` should already exist from this step

- [ ] **Step 1: Verify whether a week9 report stub is needed**

Rule:
- If user only asked for implementation planning, skip report drafting here
- If user wants immediate documentation continuity, add a one-paragraph week9 scope note later

- [ ] **Step 2: No-op by default**

No code changes unless explicitly requested.

---

## Verification Summary

Run these before claiming Week 9 foundation is complete:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/unit/transformer -q
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/integration/test_transformer_flow.py -q
UV_CACHE_DIR=/tmp/uv-cache uv run pytest -q
```

Expected:
- All transformer unit tests pass
- Ordered integration coverage passes
- Existing validate-related suite stays green

## Commit Sequence

Recommended visible history for `week9-transformer-foundation`:

1. `feat: add transformer engine foundation`
2. `feat: add type cast transformer`
3. `feat: add fill missing default strategy`
4. `feat: add fill missing drop-row strategy`
5. `feat: add dedup keep-first strategy`
6. `feat: add dedup keep-last strategy`
7. `test: add transformer foundation integration coverage`

If you want to preserve the stricter Week 7 / Week 8 style, split each feature into paired `test:` and `feat:` commits while keeping the same task order.
