# Week 11 Convert Flow Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first usable `convert` CLI flow that performs pure structured-data format conversion across `CSV`, `JSON`, and `JSONL` without validation, transformation, or reporting responsibilities.

**Architecture:** `convert` should remain the thinnest CLI flow in the project. It parses the input file based on input extension, serializes the parsed records based on output extension, and writes the output file. It must not load schema, apply transforms, filter rows, or emit reports. Failures should surface as CLI errors with clear messages.

**Tech Stack:** Python 3.12, Click, pytest, existing parser modules, new output writer utilities, TDD, small `test -> feat` commits.

---

### Task 1: Add JSON and JSONL Output Writers

**Files:**
- Modify: `src/dataguard/output.py`
- Test: `tests/unit/test_output.py`

- [ ] **Step 1: Write the failing tests**

```python
def test_write_json_output_writes_array_payload(tmp_path):
    from dataguard.output import write_json_output

    output_path = tmp_path / "records.json"
    records = [{"employee_id": "EMP-001"}, {"employee_id": "EMP-002"}]

    write_json_output(records, str(output_path))

    assert output_path.read_text(encoding="utf-8") == (
        '[\n'
        '  {\n'
        '    "employee_id": "EMP-001"\n'
        '  },\n'
        '  {\n'
        '    "employee_id": "EMP-002"\n'
        '  }\n'
        ']'
    )


def test_write_jsonl_output_writes_one_object_per_line(tmp_path):
    from dataguard.output import write_jsonl_output

    output_path = tmp_path / "records.jsonl"
    records = [{"employee_id": "EMP-001"}, {"employee_id": "EMP-002"}]

    write_jsonl_output(records, str(output_path))

    lines = output_path.read_text(encoding="utf-8").splitlines()
    assert lines == [
        '{"employee_id": "EMP-001"}',
        '{"employee_id": "EMP-002"}',
    ]
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/unit/test_output.py -q`
Expected: FAIL because `write_json_output` and `write_jsonl_output` do not exist yet

- [ ] **Step 3: Write minimal implementation**

```python
# src/dataguard/output.py
import csv
import json


def write_csv_output(records, output_path: str, fieldnames=None):
    ...


def write_json_output(records, output_path: str):
    with open(output_path, "w", encoding="utf-8") as handle:
        json.dump(records, handle, indent=2)


def write_jsonl_output(records, output_path: str):
    with open(output_path, "w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record))
            handle.write("\n")
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/unit/test_output.py -q`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/dataguard/output.py tests/unit/test_output.py
git commit -m "feat: add json and jsonl output writers"
```

---

### Task 2: Add Output Writer Factory

**Files:**
- Create: `src/dataguard/output_factory.py`
- Test: `tests/unit/test_output_factory.py`

- [ ] **Step 1: Write the failing tests**

```python
from pathlib import Path


def test_get_output_writer_returns_csv_writer_for_csv_suffix():
    from dataguard.output_factory import get_output_writer

    writer = get_output_writer(Path("out.csv"))

    assert writer.__name__ == "write_csv_output"


def test_get_output_writer_returns_json_writer_for_json_suffix():
    from dataguard.output_factory import get_output_writer

    writer = get_output_writer(Path("out.json"))

    assert writer.__name__ == "write_json_output"


def test_get_output_writer_returns_jsonl_writer_for_jsonl_suffix():
    from dataguard.output_factory import get_output_writer

    writer = get_output_writer(Path("out.jsonl"))

    assert writer.__name__ == "write_jsonl_output"


def test_get_output_writer_raises_for_unsupported_suffix():
    from dataguard.output_factory import get_output_writer

    try:
        get_output_writer(Path("out.txt"))
    except ValueError as exc:
        assert "Unsupported output format" in str(exc)
    else:
        raise AssertionError("Expected ValueError for unsupported output format")
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/unit/test_output_factory.py -q`
Expected: FAIL with import error

- [ ] **Step 3: Write minimal implementation**

```python
# src/dataguard/output_factory.py
from pathlib import Path

from dataguard.output import write_csv_output, write_json_output, write_jsonl_output


def get_output_writer(path: Path):
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return write_csv_output
    if suffix == ".json":
        return write_json_output
    if suffix == ".jsonl":
        return write_jsonl_output
    raise ValueError(f"Unsupported output format: {suffix or '<none>'}")
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/unit/test_output_factory.py -q`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/dataguard/output_factory.py tests/unit/test_output_factory.py
git commit -m "feat: add output writer factory"
```

---

### Task 3: Add Convert CLI Contract

**Files:**
- Modify: `src/dataguard/cli.py`
- Modify: `tests/cli/test_cli.py`

- [ ] **Step 1: Write the failing test**

```python
def test_convert_requires_input_and_output_paths():
    from click.testing import CliRunner
    from dataguard.cli import main

    runner = CliRunner()
    result = runner.invoke(main, ["convert", "--input", "in.csv"])

    assert result.exit_code == 2
```

- [ ] **Step 2: Run test to verify it fails**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/cli/test_cli.py::test_convert_requires_input_and_output_paths -q`
Expected: FAIL because `convert` command does not exist yet

- [ ] **Step 3: Add minimal CLI signature**

```python
@main.command()
@click.option("--input", "input_path", required=True)
@click.option("--output", "output_path", required=True)
def convert(input_path, output_path):
    raise NotImplementedError
```

- [ ] **Step 4: Run test to verify contract passes**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/cli/test_cli.py::test_convert_requires_input_and_output_paths -q`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/dataguard/cli.py tests/cli/test_cli.py
git commit -m "test: add convert cli contract"
```

---

### Task 4: Implement Core Convert Flow

**Files:**
- Modify: `src/dataguard/cli.py`
- Reuse: `src/dataguard/parser/factory.py`
- Reuse: `src/dataguard/output_factory.py`
- Test: `tests/integration/test_convert_flow.py`
- Fixture: `tests/fixtures/convert/valid/csv_convert_valid.csv`

- [ ] **Step 1: Write the failing integration test**

```python
import json
from pathlib import Path

from click.testing import CliRunner

from dataguard.cli import main


def test_convert_flow_csv_to_json_writes_output(tmp_path):
    runner = CliRunner()
    fixture_root = Path(__file__).parent.parent / "fixtures" / "convert"
    input_path = fixture_root / "valid" / "csv_convert_valid.csv"
    output_path = tmp_path / "converted.json"

    result = runner.invoke(
        main,
        [
            "convert",
            "--input", str(input_path),
            "--output", str(output_path),
        ],
    )

    assert result.exit_code == 0, result.output
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload[0]["employee_id"] == "EMP-001"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/integration/test_convert_flow.py::test_convert_flow_csv_to_json_writes_output -q`
Expected: FAIL because `convert` is not implemented

- [ ] **Step 3: Implement thin convert orchestration**

```python
@main.command()
@click.option("--input", "input_path", required=True)
@click.option("--output", "output_path", required=True)
def convert(input_path, output_path):
    try:
        parser = get_parser(Path(input_path))
    except ValueError as exc:
        raise click.ClickException(str(exc)) from exc

    try:
        writer = get_output_writer(Path(output_path))
    except ValueError as exc:
        raise click.ClickException(str(exc)) from exc

    try:
        parse_result = parser.parse(input_path)
    except FileNotFoundError as exc:
        raise click.ClickException("Input file not found") from exc
    except ParseFailure as exc:
        raise click.ClickException(str(exc)) from exc

    writer(parse_result.records, output_path)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/integration/test_convert_flow.py::test_convert_flow_csv_to_json_writes_output -q`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/dataguard/cli.py src/dataguard/output_factory.py tests/integration/test_convert_flow.py tests/fixtures/convert/valid/csv_convert_valid.csv
git commit -m "feat: add core convert flow"
```

---

### Task 5: Add JSON to JSONL Coverage

**Files:**
- Modify: `tests/integration/test_convert_flow.py`
- Fixture: `tests/fixtures/convert/valid/json_convert_valid.json`

- [ ] **Step 1: Write the failing integration test**

```python
def test_convert_flow_json_to_jsonl_writes_line_delimited_output(tmp_path):
    runner = CliRunner()
    fixture_root = Path(__file__).parent.parent / "fixtures" / "convert"
    input_path = fixture_root / "valid" / "json_convert_valid.json"
    output_path = tmp_path / "converted.jsonl"

    result = runner.invoke(
        main,
        [
            "convert",
            "--input", str(input_path),
            "--output", str(output_path),
        ],
    )

    assert result.exit_code == 0, result.output
    lines = output_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    assert '"employee_id": "EMP-001"' in lines[0]
```

- [ ] **Step 2: Run test to verify it fails if writer path is incomplete**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/integration/test_convert_flow.py::test_convert_flow_json_to_jsonl_writes_line_delimited_output -q`
Expected: FAIL until JSONL output path is fully wired

- [ ] **Step 3: Fix any serializer gaps**

Expected implementation scope:
- Ensure JSON array input is parsed into records
- Ensure JSONL writer emits one JSON object per line

- [ ] **Step 4: Run test to verify it passes**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/integration/test_convert_flow.py::test_convert_flow_json_to_jsonl_writes_line_delimited_output -q`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/integration/test_convert_flow.py tests/fixtures/convert/valid/json_convert_valid.json src/dataguard/output.py
git commit -m "test: add json to jsonl convert coverage"
```

---

### Task 6: Add JSONL to CSV Coverage

**Files:**
- Modify: `tests/integration/test_convert_flow.py`
- Fixture: `tests/fixtures/convert/valid/jsonl_convert_valid.jsonl`

- [ ] **Step 1: Write the failing integration test**

```python
def test_convert_flow_jsonl_to_csv_writes_tabular_output(tmp_path):
    runner = CliRunner()
    fixture_root = Path(__file__).parent.parent / "fixtures" / "convert"
    input_path = fixture_root / "valid" / "jsonl_convert_valid.jsonl"
    output_path = tmp_path / "converted.csv"

    result = runner.invoke(
        main,
        [
            "convert",
            "--input", str(input_path),
            "--output", str(output_path),
        ],
    )

    assert result.exit_code == 0, result.output
    content = output_path.read_text(encoding="utf-8")
    assert "employee_id" in content
    assert "EMP-001" in content
```

- [ ] **Step 2: Run test to verify it fails if CSV path is incomplete**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/integration/test_convert_flow.py::test_convert_flow_jsonl_to_csv_writes_tabular_output -q`
Expected: FAIL until full path works

- [ ] **Step 3: Fix any CSV output gaps**

Expected implementation scope:
- Ensure JSONL parser records reach CSV writer unchanged

- [ ] **Step 4: Run test to verify it passes**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/integration/test_convert_flow.py::test_convert_flow_jsonl_to_csv_writes_tabular_output -q`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/integration/test_convert_flow.py tests/fixtures/convert/valid/jsonl_convert_valid.jsonl src/dataguard/output.py
git commit -m "test: add jsonl to csv convert coverage"
```

---

### Task 7: Add JSON to CSV Coverage

**Files:**
- Modify: `tests/integration/test_convert_flow.py`
- Reuse: `tests/fixtures/convert/valid/json_convert_valid.json`

- [ ] **Step 1: Write the failing integration test**

```python
def test_convert_flow_json_to_csv_writes_csv_output(tmp_path):
    runner = CliRunner()
    fixture_root = Path(__file__).parent.parent / "fixtures" / "convert"
    input_path = fixture_root / "valid" / "json_convert_valid.json"
    output_path = tmp_path / "converted.csv"

    result = runner.invoke(
        main,
        [
            "convert",
            "--input", str(input_path),
            "--output", str(output_path),
        ],
    )

    assert result.exit_code == 0, result.output
    content = output_path.read_text(encoding="utf-8")
    assert "employee_id" in content
    assert "EMP-002" in content
```

- [ ] **Step 2: Run test to verify it fails if JSON array to CSV path is incomplete**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/integration/test_convert_flow.py::test_convert_flow_json_to_csv_writes_csv_output -q`
Expected: FAIL until path works

- [ ] **Step 3: Fix any remaining JSON array to CSV gaps**

Expected implementation scope:
- No behavior beyond pure format conversion

- [ ] **Step 4: Run test to verify it passes**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/integration/test_convert_flow.py::test_convert_flow_json_to_csv_writes_csv_output -q`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/integration/test_convert_flow.py tests/fixtures/convert/valid/json_convert_valid.json src/dataguard/output.py
git commit -m "test: add json to csv convert coverage"
```

---

### Task 8: Add Convert Error Handling Coverage

**Files:**
- Modify: `tests/integration/test_convert_flow.py`
- Modify: `src/dataguard/cli.py` only if needed

- [ ] **Step 1: Write failing tests for CLI errors**

```python
def test_convert_reports_missing_input_file():
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "convert",
            "--input", "missing.csv",
            "--output", "out.json",
        ],
    )

    assert result.exit_code == 1
    assert "Input file not found" in result.output


def test_convert_reports_unsupported_output_format(tmp_path):
    runner = CliRunner()
    fixture_root = Path(__file__).parent.parent / "fixtures" / "convert"
    input_path = fixture_root / "valid" / "csv_convert_valid.csv"
    output_path = tmp_path / "out.txt"

    result = runner.invoke(
        main,
        [
            "convert",
            "--input", str(input_path),
            "--output", str(output_path),
        ],
    )

    assert result.exit_code == 1
    assert "Unsupported output format" in result.output
```

- [ ] **Step 2: Run tests to verify they fail where expected**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/integration/test_convert_flow.py -q`
Expected: Some FAIL until error handling is aligned

- [ ] **Step 3: Align CLI error handling**

Expected implementation scope:
- Missing input file -> `click.ClickException("Input file not found")`
- Unsupported output format -> `click.ClickException(...)`
- Unsupported input format -> `click.ClickException(...)`
- Invalid parse payload -> surfaced parse failure

- [ ] **Step 4: Run tests to verify they pass**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/integration/test_convert_flow.py -q`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/dataguard/cli.py tests/integration/test_convert_flow.py
git commit -m "test: add convert error handling coverage"
```

---

### Task 9: Run Full Regression Suite

**Files:**
- No source changes required unless regressions surface

- [ ] **Step 1: Run the full test suite**

Run:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run pytest -q
```

Expected:
- All existing `validate` tests pass
- All existing `transformer` tests pass
- All existing `clean` tests pass
- All new `convert` tests pass

- [ ] **Step 2: Fix regressions if any appear**

Allowed scope:
- Small compatibility fixes only
- Do not expand `convert` beyond pure format conversion

- [ ] **Step 3: Commit regression fixes if needed**

Example:

```bash
git add <affected files>
git commit -m "fix: resolve convert regression issues"
```

---

## Week 11 Deliverables

By the end of Week 11, the repository should include:

- `convert` CLI command in `src/dataguard/cli.py`
- Output writers for `CSV`, `JSON`, and `JSONL`
- Output writer factory for suffix-based dispatch
- `convert` integration coverage for:
  - `CSV -> JSON`
  - `JSON -> JSONL`
  - `JSONL -> CSV`
  - `JSON -> CSV`
- Convert error handling coverage
- A clean separation of responsibilities:
  - `validate` handles schema validation and reports
  - `clean` handles transforms + validation + filtered output + reports
  - `convert` handles pure format conversion only

---

## Out of Scope

Week 11 does **not** include:

- Schema loading in `convert`
- Validation during `convert`
- Transform application during `convert`
- JSON/text report generation for `convert`
- Additional transformer operations such as:
  - `date_format`
  - `field_map`
  - `forward_fill`
  - `mean`
  - `dedup keep=none`

---

## Success Criteria

Week 11 is complete when:

- `convert` can read `CSV`, `JSON`, and `JSONL`
- `convert` can write `CSV`, `JSON`, and `JSONL`
- The four representative conversion paths pass in integration tests
- Error handling is aligned with existing CLI conventions
- Full pytest suite passes
- The implementation stays thin and does not absorb `validate` or `clean` responsibilities
