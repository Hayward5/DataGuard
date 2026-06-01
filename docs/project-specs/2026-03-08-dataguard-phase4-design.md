# DataGuard Phase 4 Design

Date: 2026-03-08

## Goal
Implement report generation (text + JSON) and CLI commands (validate/convert/clean) with clear error handling and configurable report detail limits.

## Scope Decisions
- CLI includes validate, convert, clean commands
- Reporter only renders output; CLI assembles Report model
- `--report` is required for validate and clean; output is always written to file
- Error handling: short stderr message, exit code 1 for runtime errors
- Text/JSON reports include summary + per-column stats + first N error details (default 20, configurable)

## Architecture Overview
- reporter/ handles formatting and output only
- CLI orchestrates parsing, validation, transformation, and report assembly
- Report model is built in CLI layer from ValidationResult + metadata
- Reporter functions accept Report model and output format settings

## Data Flow
validate:
  parse input -> load schema -> validate records -> build Report -> write report

convert:
  parse input -> write output (format determined by output file extension)

clean:
  parse input -> load transforms -> apply transforms -> validate transformed records -> filter valid rows -> write clean output -> write report

## Report Content
Text report:
- Summary: total, pass/warning/error counts
- Parse errors: row and message for each parse error
- Validation error details: first N items (row, column, code, message)

JSON report:
- Summary: source_file, schema_name, timestamp, total_rows, pass_count, warning_count, parse_error_count, validation_error_count, error_count
- error_summary: error codes per column
- parse_errors: row and message for each parse error
- details: first N validation result items (row, column, value, level, code, message)
- Limit N configurable by CLI parameter (default 20)

Current decision note: `warning_count` remains in the report shape for compatibility, but current validators do not emit warnings and this behavior is intentionally not being changed.

## CLI Behavior
- validate --input --schema --report [--format json|text] [--limit N]
- convert --input --output
- clean --input --schema --transforms --output --report [--format json|text] [--limit N]

Errors:
- Print short stderr message
- Exit code 1 for runtime errors (file not found, invalid schema, parse failure, unsupported format)
- Exit code 2 for CLI usage errors (missing required options)

## Design Approval
Approved by user for:
- Full Phase 4 scope (text/json reports + validate/convert/clean)
- Report detail level and configurable limit
- `--report` required for validate and clean
- Error handling with exit code 1 for runtime errors
