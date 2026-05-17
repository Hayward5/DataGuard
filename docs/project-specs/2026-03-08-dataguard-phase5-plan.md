# DataGuard Phase 5 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build integration tests and fixtures for validate/convert/clean flows across CSV, JSON, and JSONL with edge cases.

**Architecture:** Integration tests drive CLI commands using fixtures in tests/fixtures/<flow>/<valid|invalid|edge>. Each test asserts exit codes, output files, and report structures.

**Tech Stack:** Python 3.10+, pytest, click

---

### Task 1: Create validate fixtures (CSV/JSON/JSONL)

**Files:**
- Create: `tests/fixtures/validate/valid/csv_employees_valid.csv`
- Create: `tests/fixtures/validate/valid/json_employees_valid.json`
- Create: `tests/fixtures/validate/valid/jsonl_employees_valid.jsonl`
- Create: `tests/fixtures/validate/invalid/csv_employees_invalid.csv`
- Create: `tests/fixtures/validate/invalid/json_employees_invalid.json`
- Create: `tests/fixtures/validate/invalid/jsonl_employees_invalid.jsonl`
- Create: `tests/fixtures/validate/edge/csv_employees_edge_empty.csv`
- Create: `tests/fixtures/validate/edge/json_employees_edge_missing_field.json`
- Create: `tests/fixtures/validate/edge/jsonl_employees_edge_bad_line.jsonl`

**Step 1: Write minimal fixtures**

```text
# csv_employees_valid.csv
employee_id,name,age
EMP-00001,Alice,30
EMP-00002,Bob,40
```

```json
// json_employees_valid.json
[
  {"employee_id": "EMP-00001", "name": "Alice", "age": 30},
  {"employee_id": "EMP-00002", "name": "Bob", "age": 40}
]
```

```text
# jsonl_employees_valid.jsonl
{"employee_id": "EMP-00001", "name": "Alice", "age": 30}
{"employee_id": "EMP-00002", "name": "Bob", "age": 40}
```

**Step 2: Create invalid fixtures**

```text
# csv_employees_invalid.csv
employee_id,name,age
EMP-00001,Alice,abc
```

```json
// json_employees_invalid.json
[
  {"employee_id": "EMP-00001", "name": "Alice", "age": "abc"}
]
```

```text
# jsonl_employees_invalid.jsonl
{"employee_id": "EMP-00001", "name": "Alice", "age": "abc"}
```

**Step 3: Create edge fixtures**

```text
# csv_employees_edge_empty.csv

```

```json
// json_employees_edge_missing_field.json
[
  {"employee_id": "EMP-00001", "age": 30}
]
```

```text
# jsonl_employees_edge_bad_line.jsonl
{"employee_id": "EMP-00001", "name": "Alice", "age": 30}
{bad json line}
```

**Step 4: Commit**

```bash
git add tests/fixtures/validate
git commit -m "Add validate fixtures" -m "Ultraworked with [Sisyphus](https://github.com/code-yeongyu/oh-my-opencode)" -m "Co-authored-by: Sisyphus <clio-agent@sisyphuslabs.ai>"
```

---

### Task 2: Create convert fixtures

**Files:**
- Create: `tests/fixtures/convert/valid/csv_to_json_valid.csv`
- Create: `tests/fixtures/convert/valid/json_to_csv_valid.json`
- Create: `tests/fixtures/convert/valid/jsonl_to_csv_valid.jsonl`
- Create: `tests/fixtures/convert/edge/csv_to_json_edge_empty.csv`
- Create: `tests/fixtures/convert/edge/json_to_csv_edge_missing_field.json`
- Create: `tests/fixtures/convert/edge/jsonl_to_csv_edge_bad_line.jsonl`

**Step 1: Write valid fixtures**

```text
# csv_to_json_valid.csv
id,name
1,Alice
2,Bob
```

```json
// json_to_csv_valid.json
[
  {"id": 1, "name": "Alice"},
  {"id": 2, "name": "Bob"}
]
```

```text
# jsonl_to_csv_valid.jsonl
{"id": 1, "name": "Alice"}
{"id": 2, "name": "Bob"}
```

**Step 2: Write edge fixtures**

```text
# csv_to_json_edge_empty.csv

```

```json
// json_to_csv_edge_missing_field.json
[
  {"id": 1}
]
```

```text
# jsonl_to_csv_edge_bad_line.jsonl
{"id": 1, "name": "Alice"}
{bad json}
```

**Step 3: Commit**

```bash
git add tests/fixtures/convert
git commit -m "Add convert fixtures" -m "Ultraworked with [Sisyphus](https://github.com/code-yeongyu/oh-my-opencode)" -m "Co-authored-by: Sisyphus <clio-agent@sisyphuslabs.ai>"
```

---

### Task 3: Create clean fixtures

**Files:**
- Create: `tests/fixtures/clean/valid/csv_clean_valid.csv`
- Create: `tests/fixtures/clean/valid/json_clean_valid.json`
- Create: `tests/fixtures/clean/valid/jsonl_clean_valid.jsonl`
- Create: `tests/fixtures/clean/invalid/csv_clean_invalid.csv`
- Create: `tests/fixtures/clean/invalid/json_clean_invalid.json`
- Create: `tests/fixtures/clean/invalid/jsonl_clean_invalid.jsonl`

**Step 1: Write valid fixtures**

```text
# csv_clean_valid.csv
employee_id,name,age
EMP-00001,Alice,30
```

```json
// json_clean_valid.json
[
  {"employee_id": "EMP-00001", "name": "Alice", "age": 30}
]
```

```text
# jsonl_clean_valid.jsonl
{"employee_id": "EMP-00001", "name": "Alice", "age": 30}
```

**Step 2: Write invalid fixtures**

```text
# csv_clean_invalid.csv
employee_id,name,age
EMP-00001,Alice,abc
```

```json
// json_clean_invalid.json
[
  {"employee_id": "EMP-00001", "name": "Alice", "age": "abc"}
]
```

```text
# jsonl_clean_invalid.jsonl
{"employee_id": "EMP-00001", "name": "Alice", "age": "abc"}
```

**Step 3: Commit**

```bash
git add tests/fixtures/clean
git commit -m "Add clean fixtures" -m "Ultraworked with [Sisyphus](https://github.com/code-yeongyu/oh-my-opencode)" -m "Co-authored-by: Sisyphus <clio-agent@sisyphuslabs.ai>"
```

---

### Task 4: Integration test for validate flow

**Files:**
- Create: `tests/integration/test_validate_flow.py`

**Step 1: Write the failing test**

```python
def test_validate_flow_csv(tmp_path):
    from dataguard.cli import main
    from click.testing import CliRunner

    runner = CliRunner()
    report_path = tmp_path / "report.json"
    result = runner.invoke(
        main,
        [
            "validate",
            "--input",
            "tests/fixtures/validate/valid/csv_employees_valid.csv",
            "--schema",
            "schemas/employees.yaml",
            "--report",
            str(report_path),
            "--format",
            "json",
        ],
    )

    assert result.exit_code == 0
    assert report_path.exists()
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/integration/test_validate_flow.py::test_validate_flow_csv -v`
Expected: FAIL until CLI validates and writes reports

**Step 3: Commit**

```bash
git add tests/integration/test_validate_flow.py
git commit -m "Add validate flow integration test" -m "Ultraworked with [Sisyphus](https://github.com/code-yeongyu/oh-my-opencode)" -m "Co-authored-by: Sisyphus <clio-agent@sisyphuslabs.ai>"
```

---

### Task 5: Integration test for convert flow

**Files:**
- Create: `tests/integration/test_convert_flow.py`

**Step 1: Write the failing test**

```python
def test_convert_flow_csv_to_json(tmp_path):
    from dataguard.cli import main
    from click.testing import CliRunner

    runner = CliRunner()
    output_path = tmp_path / "out.json"
    result = runner.invoke(
        main,
        [
            "convert",
            "--input",
            "tests/fixtures/convert/valid/csv_to_json_valid.csv",
            "--output",
            str(output_path),
        ],
    )

    assert result.exit_code == 0
    assert output_path.exists()
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/integration/test_convert_flow.py::test_convert_flow_csv_to_json -v`
Expected: FAIL until convert is implemented

**Step 3: Commit**

```bash
git add tests/integration/test_convert_flow.py
git commit -m "Add convert flow integration test" -m "Ultraworked with [Sisyphus](https://github.com/code-yeongyu/oh-my-opencode)" -m "Co-authored-by: Sisyphus <clio-agent@sisyphuslabs.ai>"
```

---

### Task 6: Integration test for clean flow

**Files:**
- Create: `tests/integration/test_clean_flow.py`

**Step 1: Write the failing test**

```python
def test_clean_flow_csv(tmp_path):
    from dataguard.cli import main
    from click.testing import CliRunner

    runner = CliRunner()
    output_path = tmp_path / "clean.csv"
    report_path = tmp_path / "report.json"
    result = runner.invoke(
        main,
        [
            "clean",
            "--input",
            "tests/fixtures/clean/valid/csv_clean_valid.csv",
            "--schema",
            "schemas/employees.yaml",
            "--output",
            str(output_path),
            "--report",
            str(report_path),
            "--format",
            "json",
        ],
    )

    assert result.exit_code == 0
    assert output_path.exists()
    assert report_path.exists()
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/integration/test_clean_flow.py::test_clean_flow_csv -v`
Expected: FAIL until clean is implemented

**Step 3: Commit**

```bash
git add tests/integration/test_clean_flow.py
git commit -m "Add clean flow integration test" -m "Ultraworked with [Sisyphus](https://github.com/code-yeongyu/oh-my-opencode)" -m "Co-authored-by: Sisyphus <clio-agent@sisyphuslabs.ai>"
```
