# Float Validator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 新增 `FloatValidator`，讓 schema 可定義 `type: float` 欄位並執行 `min`/`max` range 驗證。

**Architecture:** 新增 `src/dataguard/schema/validators/float.py`，完全對齊現有 `IntegerValidator` 結構；更新 `registry.py` 新增 `float` 分支；更新 `validators/__init__.py` 匯出新類別。`ColumnSchema.min`/`max` 已為 `float | None`，不需修改 model 層。

**Tech Stack:** Python 3.12, pytest, 現有 `BaseValidator` / `ValidationMessage` 抽象

---

## Task 1 — FloatValidator 單元測試（先寫測試）

**Files:**
- 新增：`tests/unit/schema/validators/test_float.py`

- [ ] **Step 1: 新增測試檔案**

```python
import pytest


@pytest.mark.parametrize(
    ("value", "code"),
    [
        (1.5,    "OK"),
        (0.0,    "OK"),
        (-1.5,   "OK"),
        (1,      "OK"),      # int 可轉 float
        ("3.14", "OK"),      # 字串數字可轉 float
        (0.5,    "OUT_OF_RANGE"),   # 低於 min=1.0
        (10.1,   "OUT_OF_RANGE"),   # 高於 max=10.0
        ("abc",  "INVALID_FLOAT"),
        (None,   "INVALID_FLOAT"),
    ],
)
def test_float_validator_checks_boundaries(value, code):
    from dataguard.schema.models import ColumnSchema
    from dataguard.schema.validators.float import FloatValidator

    validator = FloatValidator(
        ColumnSchema(name="score", type="float", min=1.0, max=10.0)
    )
    assert validator.validate(value).code == code


def test_float_validator_no_min_max():
    from dataguard.schema.models import ColumnSchema
    from dataguard.schema.validators.float import FloatValidator

    validator = FloatValidator(ColumnSchema(name="ratio", type="float"))
    assert validator.validate("3.14").code == "OK"
    assert validator.validate("abc").code == "INVALID_FLOAT"


def test_float_validator_boundary_values_are_valid():
    from dataguard.schema.models import ColumnSchema
    from dataguard.schema.validators.float import FloatValidator

    validator = FloatValidator(
        ColumnSchema(name="score", type="float", min=1.0, max=10.0)
    )
    assert validator.validate(1.0).code == "OK"   # 等於 min，應合法
    assert validator.validate(10.0).code == "OK"  # 等於 max，應合法
```

- [ ] **Step 2: 執行測試，確認失敗**

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/unit/schema/validators/test_float.py -v
```
預期：`ModuleNotFoundError: No module named 'dataguard.schema.validators.float'`

- [ ] **Step 3: Commit 測試**

```bash
git add tests/unit/schema/validators/test_float.py
git commit -m "test: 新增 FloatValidator 單元測試"
```

---

## Task 2 — 實作 FloatValidator

**Files:**
- 新增：`src/dataguard/schema/validators/float.py`

- [ ] **Step 1: 新增實作檔案**

```python
from dataguard.schema.validators.base import BaseValidator, ValidationMessage


class FloatValidator(BaseValidator):
    def validate(self, value) -> ValidationMessage:
        try:
            parsed = float(value)
        except (TypeError, ValueError):
            return ValidationMessage(code="INVALID_FLOAT", message="Invalid float")

        if self.schema.min is not None and parsed < self.schema.min:
            return ValidationMessage(code="OUT_OF_RANGE", message="Below min")
        if self.schema.max is not None and parsed > self.schema.max:
            return ValidationMessage(code="OUT_OF_RANGE", message="Above max")

        return ValidationMessage(code="OK", message="")
```

- [ ] **Step 2: 執行測試，確認通過**

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/unit/schema/validators/test_float.py -v
```
預期：11 passed

- [ ] **Step 3: Commit 實作**

```bash
git add src/dataguard/schema/validators/float.py
git commit -m "feat: 實作 FloatValidator"
```

---

## Task 3 — 更新 `__init__.py` 與 `registry.py`

**Files:**
- 修改：`src/dataguard/schema/validators/__init__.py`
- 修改：`src/dataguard/schema/registry.py`

- [ ] **Step 1: 更新 `__init__.py`**

在現有 imports 後加入：
```python
from dataguard.schema.validators.float import FloatValidator
```
在 `__all__` 清單加入 `"FloatValidator"`。

- [ ] **Step 2: 更新 `registry.py`**

在頂部 import 加入：
```python
from dataguard.schema.validators.float import FloatValidator
```

在 `integer` 分支之後插入：
```python
if column_schema.type == "float":
    return FloatValidator(column_schema)
```

- [ ] **Step 3: 執行既有 schema 單元測試確認不壞**

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/unit/schema/ -v
```
預期：全部通過

- [ ] **Step 4: Commit**

```bash
git add src/dataguard/schema/validators/__init__.py src/dataguard/schema/registry.py
git commit -m "feat: 在 registry 新增 float → FloatValidator 對應"
```

---

## Task 4 — 更新 registry 單元測試

**Files:**
- 修改：`tests/unit/schema/test_registry.py`

- [ ] **Step 1: 在現有測試函式加入 float 斷言**

在 `test_registry_returns_string_integer_enum_boolean_and_date_validators` 函式中新增：
```python
from dataguard.schema.validators.float import FloatValidator
# 加入斷言：
assert isinstance(
    get_validator(ColumnSchema(name="score", type="float")),
    FloatValidator,
)
```

- [ ] **Step 2: 執行確認通過**

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/unit/schema/test_registry.py -v
```

- [ ] **Step 3: Commit**

```bash
git add tests/unit/schema/test_registry.py
git commit -m "test: registry 測試涵蓋 float validator"
```

---

## Task 5 — 全套測試驗收

- [ ] **執行完整測試套件**

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run pytest -q
```
預期：原本 125 tests + 新增 float tests 全部 pass，coverage ≥ 95%
