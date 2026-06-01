# DataGuard Phase 4 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Implement reporter outputs (text + JSON) and CLI commands (validate/convert/clean) with error handling and configurable detail limits.

**Architecture:** CLI assembles a Report model from ValidationResult and metadata, then reporter modules render to text or JSON. Reporter is pure formatting; CLI orchestrates parse/validate/transform flows.

**Tech Stack:** Python 3.10+, click, pytest

---

### Task 1: Reporter models

**Files:**
- Create: `src/dataguard/reporter/models.py`
- Test: `tests/unit/reporter/test_models.py`

**Step 1: Write the failing test**

```python
def test_report_model_fields():
    from dataguard.reporter.models import Report

    report = Report(
        source_file="data.csv",
        schema_name="employees",
        timestamp="2026-03-08T00:00:00",
        total_rows=2,
        pass_count=1,
        warning_count=0,
        error_count=1,
        error_summary={"age": {"OUT_OF_RANGE": 1}},
        details=[],
    )

    assert report.source_file == "data.csv"
    assert report.error_count == 1
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/unit/reporter/test_models.py::test_report_model_fields -v`
Expected: FAIL with ImportError

**Step 3: Write minimal implementation**

```python
from dataclasses import dataclass
from typing import Any
from dataguard.schema.engine import ValidationResult


@dataclass
class Report:
    source_file: str
    schema_name: str
    timestamp: str
    total_rows: int
    pass_count: int
    warning_count: int
    error_count: int
    error_summary: dict[str, dict[str, int]]
    details: list[ValidationResult]
```

Current decision note: `warning_count` is reserved for compatibility with the report shape, but current validators do not emit warnings and this behavior is intentionally not being changed.

**Step 4: Run test to verify it passes**

Run: `uv run pytest tests/unit/reporter/test_models.py::test_report_model_fields -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/dataguard/reporter/models.py tests/unit/reporter/test_models.py
git commit -m "Add report models" -m "Ultraworked with [Sisyphus](https://github.com/code-yeongyu/oh-my-opencode)" -m "Co-authored-by: Sisyphus <clio-agent@sisyphuslabs.ai>"
```

---

### Task 2: Text report generator

**Files:**
- Create: `src/dataguard/reporter/text_report.py`
- Test: `tests/unit/reporter/test_text_report.py`

**Step 1: Write the failing test**

```python
def test_text_report_contains_summary():
    from dataguard.reporter.models import Report
    from dataguard.reporter.text_report import render_text_report

    report = Report(
        source_file="data.csv",
        schema_name="employees",
        timestamp="2026-03-08T00:00:00",
        total_rows=2,
        pass_count=1,
        warning_count=0,
        error_count=1,
        error_summary={"age": {"OUT_OF_RANGE": 1}},
        details=[],
    )

    text = render_text_report(report, limit=20)
    assert "Total Rows: 2" in text
    assert "Errors: 1" in text
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/unit/reporter/test_text_report.py::test_text_report_contains_summary -v`
Expected: FAIL with ImportError

**Step 3: Write minimal implementation**

```python
def render_text_report(report, limit: int = 20) -> str:
    lines = []
    lines.append(f"Source: {report.source_file}")
    lines.append(f"Schema: {report.schema_name}")
    lines.append(f"Total Rows: {report.total_rows}")
    lines.append(f"PASS: {report.pass_count}")
    lines.append(f"WARNING: {report.warning_count}")
    lines.append(f"Errors: {report.error_count}")
    lines.append("\nError Summary:")
    for column, codes in report.error_summary.items():
        for code, count in codes.items():
            lines.append(f"- {column}: {code} = {count}")
    lines.append("\nError Details:")
    for detail in report.details[:limit]:
        lines.append(
            f"Row {detail.row} | {detail.column} | {detail.code} | {detail.value} | {detail.message}"
        )
    return "\n".join(lines)
```

**Step 4: Run test to verify it passes**

Run: `uv run pytest tests/unit/reporter/test_text_report.py::test_text_report_contains_summary -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/dataguard/reporter/text_report.py tests/unit/reporter/test_text_report.py
git commit -m "Add text report renderer" -m "Ultraworked with [Sisyphus](https://github.com/code-yeongyu/oh-my-opencode)" -m "Co-authored-by: Sisyphus <clio-agent@sisyphuslabs.ai>"
```

---

### Task 3: JSON report generator

**Files:**
- Create: `src/dataguard/reporter/json_report.py`
- Test: `tests/unit/reporter/test_json_report.py`

**Step 1: Write the failing test**

```python
def test_json_report_contains_summary():
    from dataguard.reporter.models import Report
    from dataguard.reporter.json_report import render_json_report

    report = Report(
        source_file="data.csv",
        schema_name="employees",
        timestamp="2026-03-08T00:00:00",
        total_rows=2,
        pass_count=1,
        warning_count=0,
        error_count=1,
        error_summary={"age": {"OUT_OF_RANGE": 1}},
        details=[],
    )

    payload = render_json_report(report, limit=20)
    assert payload["summary"]["total_rows"] == 2
    assert payload["summary"]["error_count"] == 1
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/unit/reporter/test_json_report.py::test_json_report_contains_summary -v`
Expected: FAIL with ImportError

**Step 3: Write minimal implementation**

```python
def render_json_report(report, limit: int = 20) -> dict:
    return {
        "summary": {
            "source_file": report.source_file,
            "schema_name": report.schema_name,
            "timestamp": report.timestamp,
            "total_rows": report.total_rows,
            "pass_count": report.pass_count,
            "warning_count": report.warning_count,
            "error_count": report.error_count,
        },
        "error_summary": report.error_summary,
        "details": [
            {
                "row": d.row,
                "column": d.column,
                "value": d.value,
                "level": d.level,
                "code": d.code,
                "message": d.message,
            }
            for d in report.details[:limit]
        ],
    }
```

**Step 4: Run test to verify it passes**

Run: `uv run pytest tests/unit/reporter/test_json_report.py::test_json_report_contains_summary -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/dataguard/reporter/json_report.py tests/unit/reporter/test_json_report.py
git commit -m "Add JSON report renderer" -m "Ultraworked with [Sisyphus](https://github.com/code-yeongyu/oh-my-opencode)" -m "Co-authored-by: Sisyphus <clio-agent@sisyphuslabs.ai>"
```

---

### Task 4: Reporter package exports

**Files:**
- Create: `src/dataguard/reporter/__init__.py`
- Test: `tests/unit/reporter/test_reporter_exports.py`

**Step 1: Write the failing test**

```python
def test_reporter_exports():
    from dataguard.reporter import render_text_report, render_json_report
    assert render_text_report and render_json_report
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/unit/reporter/test_reporter_exports.py::test_reporter_exports -v`
Expected: FAIL with ImportError

**Step 3: Write minimal implementation**

```python
from .text_report import render_text_report
from .json_report import render_json_report
from .models import Report

__all__ = ["render_text_report", "render_json_report", "Report"]
```

**Step 4: Run test to verify it passes**

Run: `uv run pytest tests/unit/reporter/test_reporter_exports.py::test_reporter_exports -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/dataguard/reporter/__init__.py tests/unit/reporter/test_reporter_exports.py
git commit -m "Export reporter utilities" -m "Ultraworked with [Sisyphus](https://github.com/code-yeongyu/oh-my-opencode)" -m "Co-authored-by: Sisyphus <clio-agent@sisyphuslabs.ai>"
```

---

### Task 5: Report assembly helpers

**Files:**
- Create: `src/dataguard/reporter/assemble.py`
- Test: `tests/unit/reporter/test_assemble.py`

**Step 1: Write the failing test**

```python
def test_assemble_report_counts():
    from dataguard.reporter.assemble import assemble_report
    from dataguard.schema.engine import ValidationResult

    results = [
        ValidationResult(row=1, column="age", value=10, level="ERROR", code="OUT_OF_RANGE", message=""),
        ValidationResult(row=2, column="age", value=20, level="PASS", code="OK", message=""),
    ]

    report = assemble_report(
        source_file="data.csv",
        schema_name="employees",
        total_rows=2,
        results=results,
    )

    assert report.error_count == 1
    assert report.pass_count == 1
    assert report.error_summary["age"]["OUT_OF_RANGE"] == 1
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/unit/reporter/test_assemble.py::test_assemble_report_counts -v`
Expected: FAIL with ImportError

**Step 3: Write minimal implementation**

```python
from collections import defaultdict
from datetime import datetime
from dataguard.schema.engine import ValidationResult
from .models import Report


def assemble_report(source_file: str, schema_name: str, total_rows: int, results: list[ValidationResult]) -> Report:
    pass_count = sum(1 for r in results if r.level == "PASS")
    # Current decision: WARNING is reserved; validators currently do not emit it.
    warning_count = sum(1 for r in results if r.level == "WARNING")
    error_count = sum(1 for r in results if r.level == "ERROR")

    summary = defaultdict(lambda: defaultdict(int))
    for r in results:
        if r.level != "PASS":
            summary[r.column][r.code] += 1

    return Report(
        source_file=source_file,
        schema_name=schema_name,
        timestamp=datetime.utcnow().isoformat(),
        total_rows=total_rows,
        pass_count=pass_count,
        warning_count=warning_count,
        error_count=error_count,
        error_summary=summary,
        details=results,
    )
```

**Step 4: Run test to verify it passes**

Run: `uv run pytest tests/unit/reporter/test_assemble.py::test_assemble_report_counts -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/dataguard/reporter/assemble.py tests/unit/reporter/test_assemble.py
git commit -m "Add report assembly helper" -m "Ultraworked with [Sisyphus](https://github.com/code-yeongyu/oh-my-opencode)" -m "Co-authored-by: Sisyphus <clio-agent@sisyphuslabs.ai>"
```

---

### Task 6: CLI validate command

**Files:**
- Create: `src/dataguard/cli.py`
- Test: `tests/cli/test_cli.py`

**Step 1: Write the failing test**

```python
def test_cli_validate_missing_args():
    from dataguard.cli import main
    from click.testing import CliRunner

    runner = CliRunner()
    result = runner.invoke(main, ["validate"])

    assert result.exit_code == 2
    assert "--input" in result.output
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/cli/test_cli.py::test_cli_validate_missing_args -v`
Expected: FAIL with ImportError

**Step 3: Write minimal implementation**

```python
import click


@click.group()
def main():
    pass


@main.command()
@click.option("--input", "input_path", required=True)
@click.option("--schema", "schema_path", required=True)
@click.option("--report", "report_path")
@click.option("--format", "format", type=click.Choice(["text", "json"]), default="text")
@click.option("--limit", "limit", type=int, default=20)
def validate(input_path, schema_path, report_path, format, limit):
    if report_path is None:
        raise click.UsageError("--report is required for output")


@main.command()
@click.option("--input", "input_path", required=True)
@click.option("--output", "output_path", required=True)
def convert(input_path, output_path):
    pass


@main.command()
@click.option("--input", "input_path", required=True)
@click.option("--schema", "schema_path", required=True)
@click.option("--output", "output_path", required=True)
@click.option("--report", "report_path")
@click.option("--format", "format", type=click.Choice(["text", "json"]), default="text")
@click.option("--limit", "limit", type=int, default=20)
def clean(input_path, schema_path, output_path, report_path, format, limit):
    if report_path is None:
        raise click.UsageError("--report is required for output")
```

**Step 4: Run test to verify it passes**

Run: `uv run pytest tests/cli/test_cli.py::test_cli_validate_missing_args -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/dataguard/cli.py tests/cli/test_cli.py
git commit -m "Add CLI commands" -m "Ultraworked with [Sisyphus](https://github.com/code-yeongyu/oh-my-opencode)" -m "Co-authored-by: Sisyphus <clio-agent@sisyphuslabs.ai>"
```

---

### Task 7: CLI validate flow integration

**Files:**
- Modify: `src/dataguard/cli.py`
- Test: `tests/cli/test_cli.py`

**Step 1: Write the failing test**

```python
def test_cli_validate_requires_report_path():
    from dataguard.cli import main
    from click.testing import CliRunner

    runner = CliRunner()
    result = runner.invoke(main, ["validate", "--input", "data.csv", "--schema", "schema.yaml"])

    assert result.exit_code == 2
    assert "--report is required" in result.output
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/cli/test_cli.py::test_cli_validate_requires_report_path -v`
Expected: FAIL before implementation

**Step 3: Implement error handling**

```python
@main.command()
@click.option("--input", "input_path", required=True)
@click.option("--schema", "schema_path", required=True)
@click.option("--report", "report_path")
@click.option("--format", "format", type=click.Choice(["text", "json"]), default="text")
@click.option("--limit", "limit", type=int, default=20)
def validate(input_path, schema_path, report_path, format, limit):
    if report_path is None:
        raise click.UsageError("--report is required for output")
```

**Step 4: Run test to verify it passes**

Run: `uv run pytest tests/cli/test_cli.py::test_cli_validate_requires_report_path -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/dataguard/cli.py tests/cli/test_cli.py
git commit -m "Enforce report output for validate" -m "Ultraworked with [Sisyphus](https://github.com/code-yeongyu/oh-my-opencode)" -m "Co-authored-by: Sisyphus <clio-agent@sisyphuslabs.ai>"
```

---

### Task 8: Reporter unit test run

**Files:**
- Modify: none
- Test: `tests/unit/reporter/`

**Step 1: Run reporter unit tests**

Run: `uv run pytest tests/unit/reporter -v`
Expected: PASS

**Step 2: Commit (if needed)**

```bash
git add tests/unit/reporter
git commit -m "Test reporter outputs" -m "Ultraworked with [Sisyphus](https://github.com/code-yeongyu/oh-my-opencode)" -m "Co-authored-by: Sisyphus <clio-agent@sisyphuslabs.ai>"
```
