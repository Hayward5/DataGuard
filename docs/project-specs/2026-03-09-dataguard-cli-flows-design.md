# DataGuard CLI Flows Design

**Goal:** Design the thin CLI orchestration layer for validate, convert, and clean flows.

**Architecture:** CLI commands (click) serve as thin wrappers around the core components (parser, schema, transformer, reporter). They handle argument parsing, file IO orchestration, and exit code management.

**Tech Stack:** Python 3.12+, Click, dataguard.parser, dataguard.schema, dataguard.transformer, dataguard.reporter

---

## 1. CLI Command Structure

The CLI at `src/dataguard/cli.py` implements three primary flows:

### 1.1 Validate Flow
- Purpose: Check input file against a schema and produce a validation report.
- Command: `dataguard validate --input <path> --schema <path> --report <path> [--format <json|text>] [--limit N]`
- `--report` is required.
- Success: Exit 0 (no ERROR-level results)
- Failure: Exit 1 (one or more ERROR-level results)

### 1.2 Convert Flow
- Purpose: Convert input file to a different format without validation or transformation.
- Command: `dataguard convert --input <path> --output <path>`
- Output format is inferred from the `--output` file extension.
- Success: Exit 0
- Failure: Exit 1 (unsupported format, file not found, or fatal parse error)

**JSONL partial parse behavior:** When the input is JSONL and some lines are malformed, convert performs best-effort conversion. Valid lines are converted and written to output; malformed lines are silently skipped. The command exits 0 if output writing succeeds. For JSON array input, a malformed file is a fatal error and exits 1.

### 1.3 Clean Flow
- Purpose: Apply transforms, validate transformed records, and produce a clean output file containing only valid records.
- Command: `dataguard clean --input <path> --schema <path> --transforms <path> --output <path> --report <path> [--format <json|text>] [--limit N]`
- `--report` is required.
- Success: Exit 0 (all transformed records pass validation)
- Failure: Exit 1 (any transformed record has ERROR, or critical failure)

---

## 2. Data Flow Orchestration

### 2.1 Validate Data Flow
1. Parse input: Use `dataguard.parser` to parse records.
2. Load schema: Use `dataguard.schema.loader` to parse schema.
3. Validate records: Pass records to `dataguard.schema.engine.validate_records`.
4. Assemble report: Build `Report` from `ValidationResult` list and parse errors.
5. Write report: Use `dataguard.reporter` to render and write report to `--report`.
6. Exit code: Return 1 if any result has level `ERROR` or any parse error exists.

### 2.2 Convert Data Flow
1. Parse input: Use `dataguard.parser` to parse records.
2. Determine output format: Infer from `--output` extension (.csv, .json, .jsonl).
3. Write output: Use `dataguard.output_factory` to serialize records to `--output`.
4. Exit code: Return 0 on success, 1 on fatal error.

### 2.3 Clean Data Flow
1. Parse input: Use `dataguard.parser` to parse records.
2. Load schema: Use `dataguard.schema.loader` to parse schema.
3. Load transforms: Use `dataguard.transformer.loader` to load transforms YAML.
4. Apply transforms: Use `dataguard.transformer.engine.apply_transforms` to transform records.
5. Validate transformed records: Use `dataguard.schema.engine.validate_records`.
6. Filter: Keep records with no ERROR-level results; drop ERROR records.
7. Write clean output: Write filtered records to `--output` (CSV format).
8. Assemble and write report: Build `Report` and write to `--report`.
9. Exit code: Return 1 if any transformed record had ERROR, otherwise 0.

---

## 3. Error Handling & Exit Codes

| Scenario | Behavior | Exit Code |
|----------|----------|-----------|
| Validation ERROR found | Report written with details | 1 |
| Validation PASS/WARNING only | Report written | 0 |
| File not found | Error message to stderr | 1 |
| Invalid schema | Error message to stderr | 1 |
| Fatal parse error (e.g. malformed JSON array) | Error message to stderr | 1 |
| Unsupported input/output format | Error message to stderr | 1 |
| Missing required CLI option | Click usage error message | 2 |

---

Current decision note: `WARNING` remains reserved for report compatibility, but current validators do not emit warnings. The PASS/WARNING wording is retained from the original design and is intentionally not being expanded now.

## 4. Reporting Format (JSON)

Validation reports follow this structure:
```json
{
  "summary": {
    "source_file": "employees.csv",
    "schema_name": "employees",
    "timestamp": "2026-05-17T10:00:00+00:00",
    "total_rows": 10,
    "pass_count": 7,
    "warning_count": 0,
    "parse_error_count": 0,
    "validation_error_count": 3,
    "error_count": 3
  },
  "error_summary": {
    "age": {"OUT_OF_RANGE": 1, "INVALID_INTEGER": 1},
    "status": {"INVALID_ENUM": 1}
  },
  "parse_errors": [
    {"row": 2, "message": "Expecting property name enclosed in double quotes"}
  ],
  "details": [
    {
      "row": 3,
      "column": "age",
      "value": "abc",
      "level": "ERROR",
      "code": "INVALID_INTEGER",
      "message": "Invalid integer"
    }
  ]
}
```

---

## 5. Testing Strategy

### 5.1 Integration Tests
Located in `tests/integration/`:
- `test_validate_flow.py`: Verifies `validate` command with valid/invalid/edge fixtures.
- `test_convert_flow.py`: Verifies `convert` command across formats and edge cases.
- `test_clean_flow.py`: Verifies `clean` command correctly transforms, validates, and filters records.

### 5.2 Assertions
- `result.exit_code` matches expected value.
- Output files exist and contain expected data.
- Report files contain correct error codes and structure.
