# DataGuard CLI Flows Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Implement the validate, convert, and clean CLI flows in `src/dataguard/cli.py` to orchestrate parser, schema, and reporter components.

**Architecture:** CLI commands serve as thin orchestration layers. They handle file IO (reading via parsers, writing via serializers/reporters), invoke the validation engine, and manage exit codes (0 for success, 1 for errors).

**Tech Stack:** Python 3.10+, Click, dataguard.parser, dataguard.schema, dataguard.reporter

**Note:** Commit only if user explicitly requests.

---

### Task 1: CLI Validate Flow Orchestration

**Files:**
- Modify: `src/dataguard/cli.py`
- Test: `tests/integration/test_validate_flow.py`

**Step 1: Write the failing test**

Already exists as `tests/integration/test_validate_flow.py`.

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/integration/test_validate_flow.py::test_validate_flow_csv -v`
Expected: FAIL (likely exit code 0 or missing report file since `validate` is currently a `pass`)

**Step 3: Implement Validate Flow**

```python
import click
from pathlib import Path
from dataguard.parser.csv_parser import CsvParser
from dataguard.parser.json_parser import JsonParser
from dataguard.schema.loader import load_schema
from dataguard.schema.engine import validate_records
from dataguard.reporter.assemble import assemble_report
from dataguard.reporter import render_json_report, render_text_report

def get_parser(file_path: str):
    ext = Path(file_path).suffix.lower()
    if ext == ".csv":
        return CsvParser()
    if ext in [".json", ".jsonl"]:
        return JsonParser()
    raise click.ClickException(f"Unsupported input format: {ext}")

@main.command()
@click.option("--input", "input_path", required=True)
@click.option("--schema", "schema_path", required=True)
@click.option("--report", "report_path")
@click.option("--format", "report_format", type=click.Choice(["text", "json"]), default="text")
@click.option("--limit", "limit", type=int, default=20)
def validate(input_path, schema_path, report_path, report_format, limit):
    if not report_path:
        raise click.UsageError("--report is required for output")

    # 1. Load Schema
    schema = load_schema(schema_path)

    # 2. Parse Input
    parser = get_parser(input_path)
    parse_result = parser.parse(input_path)
    
    # 3. Validate
    results = validate_records(schema, parse_result.records)
    
    # 4. Assemble Report
    report_obj = assemble_report(
        source_file=input_path,
        schema_name=schema.name,
        total_rows=len(parse_result.records),
        results=results
    )
    
    # 5. Render & Write Report
    if report_format == "json":
        content = render_json_report(report_obj, limit=limit)
        import json
        with open(report_path, "w") as f:
            json.dump(content, f, indent=2)
    else:
        content = render_text_report(report_obj, limit=limit)
        with open(report_path, "w") as f:
            f.write(content)
            
    # 6. Exit Code
    if report_obj.error_count > 0:
        import sys
        sys.exit(1)
```

**Step 4: Run test to verify it passes**

Run: `uv run pytest tests/integration/test_validate_flow.py::test_validate_flow_csv -v`
Expected: PASS

---

### Task 2: CLI Convert Flow Orchestration

**Files:**
- Modify: `src/dataguard/cli.py`
- Test: `tests/integration/test_convert_flow.py`

**Step 1: Write the failing test**

Already exists as `tests/integration/test_convert_flow.py`.

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/integration/test_convert_flow.py::test_convert_flow_csv_to_json -v`
Expected: FAIL

**Step 3: Implement Convert Flow**

```python
def write_output(records, output_path):
    ext = Path(output_path).suffix.lower()
    if ext == ".csv":
        import csv
        if not records: return
        keys = records[0].keys()
        with open(output_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(records)
    elif ext == ".json":
        import json
        with open(output_path, "w") as f:
            json.dump(records, f, indent=2)
    elif ext == ".jsonl":
        import json
        with open(output_path, "w") as f:
            for r in records:
                f.write(json.dumps(r) + "\n")
    else:
        raise click.ClickException(f"Unsupported output format: {ext}")

@main.command()
@click.option("--input", "input_path", required=True)
@click.option("--output", "output_path", required=True)
def convert(input_path, output_path):
    parser = get_parser(input_path)
    parse_result = parser.parse(input_path)
    if parse_result.errors:
        click.echo(f"Parse errors encountered in {input_path}", err=True)
        import sys
        sys.exit(1)
        
    write_output(parse_result.records, output_path)
```

**Step 4: Run test to verify it passes**

Run: `uv run pytest tests/integration/test_convert_flow.py::test_convert_flow_csv_to_json -v`
Expected: PASS

---

### Task 3: CLI Clean Flow Orchestration

**Files:**
- Modify: `src/dataguard/cli.py`
- Test: `tests/integration/test_clean_flow.py`

**Step 1: Write the failing test**

Already exists as `tests/integration/test_clean_flow.py`.

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/integration/test_clean_flow.py::test_clean_flow_csv -v`
Expected: FAIL

**Step 3: Implement Clean Flow**

```python
@main.command()
@click.option("--input", "input_path", required=True)
@click.option("--schema", "schema_path", required=True)
@click.option("--output", "output_path", required=True)
@click.option("--report", "report_path")
@click.option("--format", "report_format", type=click.Choice(["text", "json"]), default="text")
@click.option("--limit", "limit", type=int, default=20)
def clean(input_path, schema_path, output_path, report_path, report_format, limit):
    if not report_path:
        raise click.UsageError("--report is required for output")

    # 1. Load Schema
    schema = load_schema(schema_path)

    # 2. Parse Input
    parser = get_parser(input_path)
    parse_result = parser.parse(input_path)
    
    # 3. Validate
    results = validate_records(schema, parse_result.records)
    
    # 4. Filter records (keep PASS/WARNING, drop ERROR)
    # Current decision: WARNING is reserved; validators currently do not emit it.
    # Note: validate_records returns list of ValidationResult. 
    # Need to group results by row to filter records.
    from collections import defaultdict
    row_errors = defaultdict(bool)
    for res in results:
        if res.level == "ERROR":
            row_errors[res.row] = True
            
    clean_records = [
        rec for i, rec in enumerate(parse_result.records, start=1)
        if not row_errors[i]
    ]
    
    # 5. Write Clean Output
    write_output(clean_records, output_path)
    
    # 6. Assemble & Write Report
    report_obj = assemble_report(
        source_file=input_path,
        schema_name=schema.name,
        total_rows=len(parse_result.records),
        results=results
    )
    
    if report_format == "json":
        import json
        content = render_json_report(report_obj, limit=limit)
        with open(report_path, "w") as f:
            json.dump(content, f, indent=2)
    else:
        content = render_text_report(report_obj, limit=limit)
        with open(report_path, "w") as f:
            f.write(content)
            
    # 7. Exit Code
    if report_obj.error_count > 0:
        import sys
        sys.exit(1)
```

**Step 4: Run test to verify it passes**

Run: `uv run pytest tests/integration/test_clean_flow.py::test_clean_flow_csv -v`
Expected: PASS

---

### Task 4: Final Integration Verification

**Step 1: Run all integration tests**

Run: `uv run pytest tests/integration -v`
Expected: 3 PASS (test_validate_flow, test_convert_flow, test_clean_flow)

**Step 2: Verify results with user**

Note: Commit only if user explicitly requests.
