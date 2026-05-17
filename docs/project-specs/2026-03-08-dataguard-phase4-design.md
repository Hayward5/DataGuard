# DataGuard Phase 4 Design

Date: 2026-03-08

## Goal
Implement report generation (text + JSON) and CLI commands (validate/convert/clean) with clear error handling and configurable report detail limits.

## Scope Decisions
- CLI includes validate, convert, clean commands
- Reporter only renders output; CLI assembles Report model
- Default output writes to file only when --report is provided
- Error handling: short stderr message + suggestion, exit code 2
- Text/JSON reports include summary + per-column stats + first N error details (default 20, configurable)

## Architecture Overview
- reporter/ handles formatting and output only
- CLI orchestrates parsing, validation, transformation, and report assembly
- Report model is built in CLI layer from ValidationResult + metadata
- Reporter functions accept Report model and output format settings

## Data Flow
validate:
  read input -> parse -> load schema -> validate -> build Report -> write report

convert:
  read input -> transform -> write output

clean:
  read input -> validate -> transform -> write output -> write report

## Report Content
Text report:
- Summary: total, pass/warning/error counts
- Column stats: error codes per column
- Error details: first N items (row, column, value, code, message)

JSON report:
- Summary + column stats + first N error details
- Limit N configurable by CLI parameter (default 20)

## CLI Behavior
- validate --input --schema [--report] [--format text|json] [--limit N]
- convert --input --output
- clean --input --schema --output [--report] [--format text|json] [--limit N]

Errors:
- Print short stderr message + suggestion
- Exit code 2 for runtime errors

## Design Approval
Approved by user for:
- Full Phase 4 scope (text/json reports + validate/convert/clean)
- Report detail level and configurable limit
- Output behavior requiring --report for file writes
- Error handling with short stderr message and exit code 2
