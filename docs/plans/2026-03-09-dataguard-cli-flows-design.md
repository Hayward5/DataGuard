# DataGuard CLI Flows Design

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Design the thin CLI orchestration layer for validate, convert, and clean flows.

**Architecture:** CLI commands (click) serve as thin wrappers around the core components (parser, schema, transformer, reporter). They handle argument parsing, file IO orchestration, and exit code management.

**Tech Stack:** Python 3.10+, Click, dataguard.parser, dataguard.schema, dataguard.transformer, dataguard.reporter

---

## 1. CLI Command Structure

The CLI at `src/dataguard/cli.py` implements three primary flows:

### 1.1 Validate Flow
- Purpose: Check input file against a schema and produce a validation report.
- Command: `dataguard validate --input <path> --schema <path> --report <path> [--format <json|text>]`
- Success: Exit 0 (all PASS or WARNING)
- Failure: Exit 1 (one or more ERROR)

### 1.2 Convert Flow
- Purpose: Transform input file to a different format.
- Command: `dataguard convert --input <path> --output <path>`
- Success: Exit 0
- Failure: Exit 1 (IO error, parse error, or unsupported format)

### 1.3 Clean Flow
- Purpose: Validate input and produce a "clean" output file containing only valid records.
- Command: `dataguard clean --input <path> --schema <path> --output <path> --report <path> [--format <json|text>]`
- Success: Exit 0 (all records PASS/WARNING)
- Failure: Exit 1 (any record has ERROR, or critical failure)

---

## 2. Data Flow Orchestration

### 2.1 Validate Data Flow
1. Load Schema: Use `dataguard.schema.loader` to parse schema.
2. Read Input: Use `dataguard.parser` to parse records.
3. Validation: Pass records to `dataguard.schema.engine.validate_records`.
4. Result Aggregation: Collect `ValidationResult` objects.
5. Report Generation: Use `dataguard.reporter` to write report to `--report`.
6. Exit Code: Return 1 if any `ValidationResult` has level `ERROR`.

### 2.2 Convert Data Flow
1. Read Input: Use `dataguard.parser` to parse records.
2. Determine Output Format: Infer from `--output` extension (.csv, .json, .jsonl).
3. Write Output: Serialize records to the target format and write to `--output`.
4. Exit Code: Return 0 on success, 1 on any error.

### 2.3 Clean Data Flow
1. Load Schema: Use `dataguard.schema.loader` to parse schema.
2. Read Input: Use `dataguard.parser` to parse records.
3. Validation: Use `dataguard.schema.engine.validate_records`.
4. Filtering: Keep PASS/WARNING records, drop ERROR records.
5. Write Clean Output: Serialize kept records to `--output`.
6. Report Generation: Use `dataguard.reporter` to write report to `--report`.
7. Exit Code: Return 1 if any record had ERROR, otherwise 0.

---

## 3. Error Handling & Exit Codes

| Scenario | Behavior | Exit Code |
|----------|----------|-----------|
| Validation ERROR found | Report written with details | 1 |
| Validation PASS/WARNING | Report written | 0 |
| File Not Found | Error message to stderr | 1 |
| Invalid Schema | Error message to stderr | 1 |
| Parse Error (CSV/JSON) | Error message to stderr | 1 |
| IO Write Error | Error message to stderr | 1 |

---

## 4. Reporting Format (JSON)

Validation reports follow this structure:
```json
{
  "summary": {
    "total_records": 100,
    "valid_records": 95,
    "invalid_records": 5,
    "status": "ERROR"
  },
  "results": [
    {
      "row": 2,
      "column": "email",
      "level": "ERROR",
      "code": "REQUIRED_MISSING",
      "message": "Field 'email' is required"
    }
  ]
}
```

---

## 5. Testing Strategy

### 5.1 Integration Tests
Located in `tests/integration/`:
- `test_validate_flow.py`: Verifies `validate` command with valid/invalid/edge fixtures.
- `test_convert_flow.py`: Verifies `convert` command across formats.
- `test_clean_flow.py`: Verifies `clean` command correctly filters records.

### 5.2 Assertions
- `result.exit_code` matches expected value.
- Output files exist and contain expected data.
- Report files contain correct error codes (e.g., `REQUIRED_MISSING`).
