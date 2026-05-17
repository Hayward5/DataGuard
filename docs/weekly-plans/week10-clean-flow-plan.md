# Week 10 Clean Flow Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first usable `clean` CLI flow by connecting parsing, schema loading, transformer execution, validation, filtered clean output, and JSON reporting.

**Architecture:** `clean` should orchestrate existing modules instead of embedding logic inside the CLI. The flow is: parse input, load schema, load transforms, apply transforms, validate transformed records, keep only PASS rows, write clean CSV output, then write JSON report. Week 10 supports `CSV -> CSV` as the main path and adds `JSONL -> CSV` as the extra non-CSV input path.

**Tech Stack:** Python 3.12, Click, pytest, existing parser/schema/reporter/transformer modules, TDD, small `test -> feat` commits.

---

### Task 1: Add Transform Configuration Loader

**Files:**
- Create: `src/dataguard/transformer/loader.py`
- Test: `tests/unit/transformer/test_loader.py`

- [ ] **Step 1: Write the failing tests**

```python
def test_load_transforms_reads_transform_list(tmp_path):
    from dataguard.transformer.loader import load_transforms

    config_path = tmp_path / "transforms.yaml"
    config_path.write_text(
        """
transforms:
  - operation: type_cast
    column: age
    target_type: integer
  - operation: dedup
    keys: [employee_id]
    keep: last
""",
        encoding="utf-8",
    )

    transforms = load_transforms(str(config_path))

    assert transforms == [
        {"operation": "type_cast", "column": "age", "target_type": "integer"},
        {"operation": "dedup", "keys": ["employee_id"], "keep": "last"},
    ]


def test_load_transforms_returns_empty_list_when_missing_root(tmp_path):
    from dataguard.transformer.loader import load_transforms

    config_path = tmp_path / "transforms.yaml"
    config_path.write_text("{}", encoding="utf-8")

    assert load_transforms(str(config_path)) == []
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/unit/transformer/test_loader.py -q`
Expected: FAIL with import error

- [ ] **Step 3: Write minimal implementation**

```python
# src/dataguard/transformer/loader.py
import yaml


def load_transforms(file_path: str) -> list[dict]:
    with open(file_path, encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    transforms = data.get("transforms", [])
    return transforms if isinstance(transforms, list) else []
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/unit/transformer/test_loader.py -q`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/dataguard/transformer/loader.py tests/unit/transformer/test_loader.py
git commit -m "feat: add transformer config loader"
```

---

### Task 2: Add CSV Output Writer

**Files:**
- Create: `src/dataguard/output.py`
- Test: `tests/unit/test_output.py`

- [ ] **Step 1: Write the failing tests**

```python
def test_write_csv_output_writes_header_and_rows(tmp_path):
    from dataguard.output import write_csv_output

    output_path = tmp_path / "clean.csv"
    records = [
        {"employee_id": "EMP-001", "age": 20},
        {"employee_id": "EMP-002", "age": 30},
    ]

    write_csv_output(records, str(output_path))

    assert output_path.read_text(encoding="utf-8") == (
        "employee_id,age\n"
        "EMP-001,20\n"
        "EMP-002,30\n"
    )


def test_write_csv_output_writes_header_only_for_empty_records(tmp_path):
    from dataguard.output import write_csv_output

    output_path = tmp_path / "clean.csv"

    write_csv_output([], str(output_path), fieldnames=["employee_id", "age"])

    assert output_path.read_text(encoding="utf-8") == "employee_id,age\n"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/unit/test_output.py -q`
Expected: FAIL with import error

- [ ] **Step 3: Write minimal implementation**

```python
# src/dataguard/output.py
import csv


def write_csv_output(records, output_path: str, fieldnames=None):
    columns = fieldnames or (list(records[0].keys()) if records else [])
    with open(output_path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        if records:
            writer.writerows(records)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/unit/test_output.py -q`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/dataguard/output.py tests/unit/test_output.py
git commit -m "feat: add csv output writer"
```

---

### Task 3: Add Clean CLI Contract Test

**Files:**
- Modify: `tests/cli/test_cli.py`

- [ ] **Step 1: Write the failing test**

```python
def test_clean_requires_output_and_report_paths():
    from click.testing import CliRunner
    from dataguard.cli import main

    runner = CliRunner()
    result = runner.invoke(
        main,
        ["clean", "--input", "x.csv", "--schema", "schema.yaml"],
    )

    assert result.exit_code == 2
```

- [ ] **Step 2: Run test to verify it fails**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/cli/test_cli.py::test_clean_requires_output_and_report_paths -q`
Expected: FAIL because `clean` command does not exist yet

- [ ] **Step 3: Add minimal CLI signature**

```python
@main.command()
@click.option("--input", "input_path", required=True)
@click.option("--schema", "schema_path", required=True)
@click.option("--transforms", "transforms_path", required=True)
@click.option("--output", "output_path", required=True)
@click.option("--report", "report_path", required=True)
@click.option("--format", "report_format", type=click.Choice(["json"]), default="json")
@click.option("--limit", default=20, type=int)
def clean(input_path, schema_path, transforms_path, output_path, report_path, report_format, limit):
    raise NotImplementedError
```

- [ ] **Step 4: Run test to verify contract passes**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/cli/test_cli.py::test_clean_requires_output_and_report_paths -q`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/cli/test_cli.py src/dataguard/cli.py
git commit -m "test: add clean cli contract"
```

---

### Task 4: Implement CSV Clean Flow

**Files:**
- Modify: `src/dataguard/cli.py`
- Modify: `src/dataguard/reporter/assemble.py` only if additional metadata is needed
- Reuse: `src/dataguard/output.py`
- Reuse: `src/dataguard/transformer/engine.py`
- Reuse: `src/dataguard/transformer/loader.py`
- Reuse: `src/dataguard/schema/engine.py`
- Test: `tests/integration/test_clean_flow.py`
- Fixture: `tests/fixtures/clean/valid/csv_clean_valid.csv`
- Fixture: `tests/fixtures/clean/invalid/csv_clean_invalid.csv`
- Fixture: `tests/fixtures/clean/config/clean_transforms.yaml`

- [ ] **Step 1: Write the failing integration test**

```python
import json
from pathlib import Path

from click.testing import CliRunner

from dataguard.cli import main


def test_clean_flow_csv_writes_clean_output_and_json_report(tmp_path):
    runner = CliRunner()
    fixture_root = Path(__file__).parent.parent / "fixtures" / "clean"
    input_path = fixture_root / "valid" / "csv_clean_valid.csv"
    schema_path = Path(__file__).parent.parent.parent / "schemas" / "employees.yaml"
    transforms_path = fixture_root / "config" / "clean_transforms.yaml"
    output_path = tmp_path / "clean.csv"
    report_path = tmp_path / "report.json"

    result = runner.invoke(
        main,
        [
            "clean",
            "--input", str(input_path),
            "--schema", str(schema_path),
            "--transforms", str(transforms_path),
            "--output", str(output_path),
            "--report", str(report_path),
            "--format", "json",
        ],
    )

    assert result.exit_code == 0, result.output
    assert output_path.exists()
    assert report_path.exists()

    payload = json.loads(report_path.read_text(encoding="utf-8"))
    assert payload["summary"]["error_count"] == 0
```

- [ ] **Step 2: Create minimal fixtures**

```text
# tests/fixtures/clean/valid/csv_clean_valid.csv
employee_id,name,status,is_active,join_date,age
EMP-001,Alice,ACTIVE,true,2026-04-12,20
EMP-001,Alice,ACTIVE,true,2026-04-12,20
EMP-002,Bob,INACTIVE,,2026-04-10,30
```

```yaml
# tests/fixtures/clean/config/clean_transforms.yaml
transforms:
  - operation: dedup
    keys: [employee_id]
    keep: first
  - operation: fill_missing
    column: is_active
    strategy: default
    value: "false"
  - operation: type_cast
    column: age
    target_type: integer
```

- [ ] **Step 3: Run test to verify it fails**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/integration/test_clean_flow.py::test_clean_flow_csv_writes_clean_output_and_json_report -q`
Expected: FAIL until `clean` flow is implemented

- [ ] **Step 4: Implement minimal clean flow**

Required behavior:
- parse input using existing parser factory
- load schema
- load transforms
- apply transforms to parsed records
- validate transformed records
- determine which transformed rows have zero `ERROR`
- write only PASS rows to output CSV
- assemble JSON report from validation results and parse errors
- return exit code `0` when all rows are valid after transform
- return exit code `1` when any row still has validation errors or parse errors

Core implementation shape:

```python
@main.command()
@click.option("--input", "input_path", required=True)
@click.option("--schema", "schema_path", required=True)
@click.option("--transforms", "transforms_path", required=True)
@click.option("--output", "output_path", required=True)
@click.option("--report", "report_path", required=True)
@click.option("--format", "report_format", type=click.Choice(["json"]), default="json")
@click.option("--limit", default=20, type=int)
def clean(input_path, schema_path, transforms_path, output_path, report_path, report_format, limit):
    parser = get_parser(Path(input_path))
    parse_result = parser.parse(input_path)
    schema = load_schema(schema_path)
    transforms = load_transforms(transforms_path)
    transformed_records = apply_transforms(parse_result.records, transforms)
    results = validate_records(schema, transformed_records)

    row_has_error = {}
    for result in results:
        row_has_error.setdefault(result.row, False)
        if result.level == "ERROR":
            row_has_error[result.row] = True

    clean_records = [
        record
        for index, record in enumerate(transformed_records, start=1)
        if not row_has_error.get(index, False)
    ]

    write_csv_output(
        clean_records,
        output_path,
        fieldnames=list(transformed_records[0].keys()) if transformed_records else [],
    )

    report = assemble_report(
        source_file=input_path,
        schema_name=schema.name,
        total_rows=len(transformed_records),
        results=results,
        parse_errors=parse_result.errors,
    )
    payload = render_json_report(report, limit=limit)
    Path(report_path).write_text(json.dumps(payload, indent=2), encoding="utf-8")

    if report.error_count > 0:
        raise SystemExit(1)
```

- [ ] **Step 5: Run the CSV clean test**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/integration/test_clean_flow.py::test_clean_flow_csv_writes_clean_output_and_json_report -q`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add src/dataguard/cli.py src/dataguard/output.py src/dataguard/transformer/loader.py tests/integration/test_clean_flow.py tests/fixtures/clean
git commit -m "feat: add csv clean flow"
```

---

### Task 5: Add Invalid CSV Clean Coverage

**Files:**
- Modify: `tests/integration/test_clean_flow.py`
- Create: `tests/fixtures/clean/invalid/csv_clean_invalid.csv`

- [ ] **Step 1: Write the failing test**

```python
def test_clean_flow_csv_filters_invalid_rows_and_returns_exit_code_1(tmp_path):
    runner = CliRunner()
    fixture_root = Path(__file__).parent.parent / "fixtures" / "clean"
    input_path = fixture_root / "invalid" / "csv_clean_invalid.csv"
    schema_path = Path(__file__).parent.parent.parent / "schemas" / "employees.yaml"
    transforms_path = fixture_root / "config" / "clean_transforms.yaml"
    output_path = tmp_path / "clean.csv"
    report_path = tmp_path / "report.json"

    result = runner.invoke(
        main,
        [
            "clean",
            "--input", str(input_path),
            "--schema", str(schema_path),
            "--transforms", str(transforms_path),
            "--output", str(output_path),
            "--report", str(report_path),
            "--format", "json",
        ],
    )

    assert result.exit_code == 1, result.output
    assert output_path.exists()

    cleaned = output_path.read_text(encoding="utf-8")
    assert "EMP-001" in cleaned
    assert "EMP-002" not in cleaned
```

- [ ] **Step 2: Add invalid fixture**

```text
# tests/fixtures/clean/invalid/csv_clean_invalid.csv
employee_id,name,status,is_active,join_date,age
EMP-001,Alice,ACTIVE,true,2026-04-12,20
EMP-002,Robert,UNKNOWN,maybe,bad-date,abc
```

- [ ] **Step 3: Run test to verify it fails**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/integration/test_clean_flow.py::test_clean_flow_csv_filters_invalid_rows_and_returns_exit_code_1 -q`
Expected: FAIL until clean filtering behavior is correct

- [ ] **Step 4: Adjust filtering only if needed**

Expected behavior:
- valid transformed rows remain in clean output
- invalid rows are excluded
- JSON report still contains all validation errors

- [ ] **Step 5: Run clean integration suite**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/integration/test_clean_flow.py -q`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add tests/integration/test_clean_flow.py tests/fixtures/clean/invalid/csv_clean_invalid.csv
git commit -m "test: add invalid csv clean coverage"
```

---

### Task 6: Add JSONL Input Path for Clean

**Files:**
- Modify: `tests/integration/test_clean_flow.py`
- Create: `tests/fixtures/clean/valid/jsonl_clean_valid.jsonl`
- Reuse: same schema and transforms

- [ ] **Step 1: Write the failing test**

```python
def test_clean_flow_jsonl_input_writes_clean_csv_output(tmp_path):
    runner = CliRunner()
    fixture_root = Path(__file__).parent.parent / "fixtures" / "clean"
    input_path = fixture_root / "valid" / "jsonl_clean_valid.jsonl"
    schema_path = Path(__file__).parent.parent.parent / "schemas" / "employees.yaml"
    transforms_path = fixture_root / "config" / "clean_transforms.yaml"
    output_path = tmp_path / "clean.csv"
    report_path = tmp_path / "report.json"

    result = runner.invoke(
        main,
        [
            "clean",
            "--input", str(input_path),
            "--schema", str(schema_path),
            "--transforms", str(transforms_path),
            "--output", str(output_path),
            "--report", str(report_path),
            "--format", "json",
        ],
    )

    assert result.exit_code == 0, result.output
    assert output_path.exists()
```

- [ ] **Step 2: Add JSONL fixture**

```text
# tests/fixtures/clean/valid/jsonl_clean_valid.jsonl
{"employee_id": "EMP-001", "name": "Alice", "status": "ACTIVE", "is_active": "true", "join_date": "2026-04-12", "age": "20"}
{"employee_id": "EMP-001", "name": "Alice", "status": "ACTIVE", "is_active": "true", "join_date": "2026-04-12", "age": "20"}
{"employee_id": "EMP-002", "name": "Bob", "status": "INACTIVE", "is_active": "", "join_date": "2026-04-10", "age": "30"}
```

- [ ] **Step 3: Run test to verify it fails or is incomplete**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/integration/test_clean_flow.py::test_clean_flow_jsonl_input_writes_clean_csv_output -q`
Expected: FAIL until JSONL path is fully covered

- [ ] **Step 4: Adjust clean flow only if needed**

Expected minimal change:
- `get_parser()` already supports JSONL
- clean flow should work without format-specific branching as long as parser output is normalized

- [ ] **Step 5: Run clean integration suite again**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/integration/test_clean_flow.py -q`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add tests/integration/test_clean_flow.py tests/fixtures/clean/valid/jsonl_clean_valid.jsonl
git commit -m "test: add jsonl clean flow coverage"
```

---

### Task 7: Full Regression and Week 10 Verification

**Files:**
- No code changes expected

- [ ] **Step 1: Run focused clean suite**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/integration/test_clean_flow.py -q`
Expected: PASS

- [ ] **Step 2: Run full test suite**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest -q`
Expected: PASS

- [ ] **Step 3: Sanity-check clean output expectations**

Verify these behaviors:
- transformed records are validated after transforms
- only PASS rows are written to clean CSV
- invalid rows are excluded from output but remain represented in report counts
- parse errors still affect exit status and report summary

- [ ] **Step 4: Commit only if verification required code changes**

Default: no-op.

---

## Verification Summary

Run these before calling Week 10 complete:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/integration/test_clean_flow.py -q
UV_CACHE_DIR=/tmp/uv-cache uv run pytest -q
```

Expected:
- clean flow works for CSV input/output with JSON report
- JSONL input path also works with CSV clean output
- existing validate and transformer suites stay green

## Expected Week 10 Milestone

By the end of Week 10, the project should have:

- a working `clean` CLI command
- transform-before-validate orchestration
- filtered clean CSV output
- JSON report output for clean runs
- CSV main path coverage
- JSONL input coverage
- enough integration tests to demonstrate a full cleaning workflow end to end
