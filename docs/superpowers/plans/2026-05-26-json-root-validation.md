# JSON Root 結構驗證 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 讓 `JsonParser` 對非法根結構（非 array 的 JSON、非 object 的 JSONL 行）回傳明確的 `ParseFailure` 或 `ParseErrorItem`，而非靜默產生錯誤結果或 crash。

**Architecture:** 只修改 `src/dataguard/parser/json_parser.py`，在兩條解析路徑各加一層結構檢查：JSON array 路徑驗證根是 `list` 且每元素是 `dict`；JSONL 路徑在每行 parse 成功後驗證結果是 `dict`。CLI 層已有 `ParseFailure` 捕捉，無需修改。

**Tech Stack:** Python 3.12, pytest, click.testing.CliRunner（integration tests）

---

## 檔案影響範圍

| 動作 | 路徑 |
|------|------|
| 修改 | `src/dataguard/parser/json_parser.py` |
| 修改 | `tests/unit/parser/test_json_parser.py` |
| 修改 | `tests/integration/test_validate_flow.py` |
| 修改 | `tests/integration/test_convert_flow.py` |

---

## Task 1 — JSON 根為非 array 時拋 ParseFailure（unit test 先）

**Files:**
- Modify: `tests/unit/parser/test_json_parser.py`

- [ ] **Step 1: 新增失敗測試**

在 `tests/unit/parser/test_json_parser.py` 末尾加入：

```python
def test_json_parser_raises_parse_failure_when_root_is_object(tmp_path):
    import pytest
    from dataguard.exceptions import ParseFailure
    from dataguard.parser.json_parser import JsonParser

    json_path = tmp_path / "data.json"
    json_path.write_text('{"id": 1, "name": "Alice"}', encoding="utf-8")

    with pytest.raises(ParseFailure, match="must be an array"):
        JsonParser().parse(str(json_path))


def test_json_parser_raises_parse_failure_when_root_is_number(tmp_path):
    import pytest
    from dataguard.exceptions import ParseFailure
    from dataguard.parser.json_parser import JsonParser

    json_path = tmp_path / "data.json"
    json_path.write_text("42", encoding="utf-8")

    with pytest.raises(ParseFailure, match="must be an array"):
        JsonParser().parse(str(json_path))
```

- [ ] **Step 2: 執行確認失敗**

```bash
.venv/bin/pytest tests/unit/parser/test_json_parser.py::test_json_parser_raises_parse_failure_when_root_is_object tests/unit/parser/test_json_parser.py::test_json_parser_raises_parse_failure_when_root_is_number -v --override-ini="addopts="
```

預期：2 FAILED（ParseFailure 未被拋出）

- [ ] **Step 3: Commit 測試**

```bash
git add tests/unit/parser/test_json_parser.py
git commit -m "test: JSON root 非 array 應拋 ParseFailure"
```

---

## Task 2 — 實作 JSON root 結構驗證

**Files:**
- Modify: `src/dataguard/parser/json_parser.py`

- [ ] **Step 1: 在 json_parser.py 的 JSON 路徑加入根結構檢查**

將 line 27–32 的 JSON array 解析區段從：

```python
        try:
            data = json.loads(content)
        except json.JSONDecodeError as exc:
            raise ParseFailure(f"Invalid JSON input: {exc}") from exc

        return ParseResult(records=data, errors=[], metadata={})
```

改為：

```python
        try:
            data = json.loads(content)
        except json.JSONDecodeError as exc:
            raise ParseFailure(f"Invalid JSON input: {exc}") from exc

        if not isinstance(data, list):
            raise ParseFailure(
                f"JSON input must be an array of objects, got {type(data).__name__}"
            )

        records = []
        errors = []
        for index, item in enumerate(data, start=1):
            if not isinstance(item, dict):
                errors.append(
                    ParseErrorItem(
                        row=index,
                        message=f"Expected object, got {type(item).__name__}",
                    )
                )
            else:
                records.append(item)

        return ParseResult(records=records, errors=errors, metadata={})
```

- [ ] **Step 2: 執行 Task 1 的測試確認通過**

```bash
.venv/bin/pytest tests/unit/parser/test_json_parser.py -v --override-ini="addopts="
```

預期：全部通過（含原有 5 個 + 新增 2 個）

- [ ] **Step 3: Commit 實作**

```bash
git add src/dataguard/parser/json_parser.py
git commit -m "feat: JSON root 非 array 時拋 ParseFailure"
```

---

## Task 3 — JSON array 內含非 object 元素的 ParseErrorItem（unit test 先）

**Files:**
- Modify: `tests/unit/parser/test_json_parser.py`

- [ ] **Step 1: 新增失敗測試**

```python
def test_json_parser_skips_non_object_items_in_array_and_reports_error(tmp_path):
    from dataguard.parser.json_parser import JsonParser

    json_path = tmp_path / "data.json"
    json_path.write_text(
        '[{"id": 1}, "not_an_object", {"id": 2}]', encoding="utf-8"
    )

    result = JsonParser().parse(str(json_path))

    assert result.records == [{"id": 1}, {"id": 2}]
    assert len(result.errors) == 1
    assert result.errors[0].row == 2
    assert "str" in result.errors[0].message
```

- [ ] **Step 2: 執行確認通過（Task 2 的實作已包含此邏輯）**

```bash
.venv/bin/pytest tests/unit/parser/test_json_parser.py -v --override-ini="addopts="
```

預期：全部通過

- [ ] **Step 3: Commit**

```bash
git add tests/unit/parser/test_json_parser.py
git commit -m "test: JSON array 內含非 object 元素應記錄 ParseErrorItem"
```

---

## Task 4 — JSONL 每行非 object 時記錄 ParseErrorItem（unit test 先）

**Files:**
- Modify: `tests/unit/parser/test_json_parser.py`
- Modify: `src/dataguard/parser/json_parser.py`

- [ ] **Step 1: 新增失敗測試**

```python
def test_jsonl_parser_reports_error_when_line_is_not_object(tmp_path):
    from dataguard.parser.json_parser import JsonParser

    jsonl_path = tmp_path / "data.jsonl"
    jsonl_path.write_text(
        '{"id": 1}\n["not", "object"]\n{"id": 2}\n', encoding="utf-8"
    )

    result = JsonParser().parse(str(jsonl_path))

    assert result.records == [{"id": 1}, {"id": 2}]
    assert len(result.errors) == 1
    assert result.errors[0].row == 2
    assert "list" in result.errors[0].message
```

- [ ] **Step 2: 執行確認失敗**

```bash
.venv/bin/pytest tests/unit/parser/test_json_parser.py::test_jsonl_parser_reports_error_when_line_is_not_object -v --override-ini="addopts="
```

預期：FAILED（["not", "object"] 目前會被靜默收入 records）

- [ ] **Step 3: 修改 JSONL 解析路徑**

將 json_parser.py 的 JSONL 路徑（line 15–25）從：

```python
        if content.lstrip().startswith("{") and "\n" in content:
            records = []
            errors = []
            for index, line in enumerate(content.splitlines(), start=1):
                if not line.strip():
                    continue
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError as exc:
                    errors.append(ParseErrorItem(row=index, message=str(exc)))
            return ParseResult(records=records, errors=errors, metadata={})
```

改為：

```python
        if content.lstrip().startswith("{") and "\n" in content:
            records = []
            errors = []
            for index, line in enumerate(content.splitlines(), start=1):
                if not line.strip():
                    continue
                try:
                    item = json.loads(line)
                except json.JSONDecodeError as exc:
                    errors.append(ParseErrorItem(row=index, message=str(exc)))
                    continue
                if not isinstance(item, dict):
                    errors.append(
                        ParseErrorItem(
                            row=index,
                            message=f"Expected object, got {type(item).__name__}",
                        )
                    )
                else:
                    records.append(item)
            return ParseResult(records=records, errors=errors, metadata={})
```

- [ ] **Step 4: 執行確認通過**

```bash
.venv/bin/pytest tests/unit/parser/test_json_parser.py -v --override-ini="addopts="
```

預期：全部通過

- [ ] **Step 5: Commit**

```bash
git add src/dataguard/parser/json_parser.py tests/unit/parser/test_json_parser.py
git commit -m "feat: JSONL 每行非 object 時記錄 ParseErrorItem"
```

---

## Task 5 — Integration tests：validate 與 convert 對非法 JSON root 的 CLI 行為

**Files:**
- Modify: `tests/integration/test_validate_flow.py`
- Modify: `tests/integration/test_convert_flow.py`

- [ ] **Step 1: 新增 validate integration test**

在 `tests/integration/test_validate_flow.py` 末尾加入：

```python
def test_validate_reports_parse_failure_when_json_root_is_object(tmp_path):
    import json
    from pathlib import Path
    from click.testing import CliRunner
    from dataguard.cli import main

    runner = CliRunner()
    input_path = tmp_path / "bad.json"
    input_path.write_text('{"id": "EMP-001"}', encoding="utf-8")
    schema_path = Path(__file__).parent.parent.parent / "schemas" / "employees.yaml"
    report_path = tmp_path / "report.json"

    result = runner.invoke(
        main,
        [
            "validate",
            "--input", str(input_path),
            "--schema", str(schema_path),
            "--report", str(report_path),
        ],
    )

    assert result.exit_code == 1
    assert "must be an array" in result.output
```

- [ ] **Step 2: 新增 convert integration test**

在 `tests/integration/test_convert_flow.py` 末尾加入：

```python
def test_convert_reports_parse_failure_when_json_root_is_object(tmp_path):
    from click.testing import CliRunner
    from dataguard.cli import main

    runner = CliRunner()
    input_path = tmp_path / "bad.json"
    input_path.write_text('{"id": "EMP-001"}', encoding="utf-8")
    output_path = tmp_path / "out.csv"

    result = runner.invoke(
        main,
        [
            "convert",
            "--input", str(input_path),
            "--output", str(output_path),
        ],
    )

    assert result.exit_code == 1
    assert "must be an array" in result.output
```

- [ ] **Step 3: 執行確認通過**

```bash
.venv/bin/pytest tests/integration/test_validate_flow.py::test_validate_reports_parse_failure_when_json_root_is_object tests/integration/test_convert_flow.py::test_convert_reports_parse_failure_when_json_root_is_object -v --override-ini="addopts="
```

預期：2 passed

- [ ] **Step 4: Commit**

```bash
git add tests/integration/test_validate_flow.py tests/integration/test_convert_flow.py
git commit -m "test: integration tests 覆蓋 JSON root 非法結構的 CLI 行為"
```

---

## Task 6 — 全套測試驗收

- [ ] **執行完整測試套件**

```bash
.venv/bin/pytest --override-ini="addopts=" -q
```

預期：原 148 + 新增約 6 個 = 154 tests，全部 pass。
