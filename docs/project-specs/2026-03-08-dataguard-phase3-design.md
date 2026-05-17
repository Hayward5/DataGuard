# DataGuard Phase 3 Design

Date: 2026-03-08

## Goal
Add a transformer module that applies ordered, schema-driven transformations to records, supporting type casting, date formatting, missing-value strategies, deduplication, and field mapping.

## Scope Decisions
- Project root: DataGuard/
- Execution order: follows the transforms array order in YAML
- Full feature set in Phase 3: type_cast, date_format, fill_missing (default/drop_row/forward_fill/mean), dedup (keep=first default), field_map (rename + drop)

## Architecture Overview
- transformer/engine.py is the orchestrator
- Each operation is implemented as an independent function or class
- Operations are registered in an operation registry
- All transformers accept and return list[dict] (no I/O inside operations)

## Data Flow
1) CLI or higher-level layer loads transforms from YAML
2) transformer/engine.py iterates transforms in order
3) Each operation applies to records and returns updated records
4) Output is a transformed list[dict] for reporting or output writing

## YAML Transform Specification
Example:

transforms:
  - operation: "type_cast"
    column: "age"
    target_type: "integer"

  - operation: "date_format"
    column: "join_date"
    source_formats: ["%Y/%m/%d", "%m-%d-%Y"]
    target_format: "%Y-%m-%d"

  - operation: "fill_missing"
    column: "salary"
    strategy: "mean"        # default | drop_row | forward_fill | mean
    value: 0                 # used by default

  - operation: "dedup"
    keys: ["employee_id"]
    keep: "first"           # first | last | none (default: first)

  - operation: "field_map"
    rename:
      employee_id: "員工編號"
    drop:
      - "temp_note"

## Operation Behavior
- type_cast: target_type in {integer, float, string, boolean}; on cast failure keep original value
- date_format: tries source_formats in order; on failure keeps original value
- fill_missing:
  - default: fill with value
  - drop_row: remove rows with missing column
  - forward_fill: use previous non-missing value
  - mean: numeric-only; if no valid numeric values, keep original
- dedup:
  - keep=first: keep first occurrence
  - keep=last: keep last occurrence
  - keep=none: drop all duplicates
- field_map:
  - rename: renames columns; if source missing, ignore
  - drop: removes columns; if missing, ignore

## Error Handling
- Transformer functions do not raise on per-record errors
- Unknown operation names are surfaced as configuration errors at the engine level
- Use explicit error messages for invalid rule formats or missing required fields

## Testing Strategy
- Unit tests per transformer function for normal and edge cases
- Decision-table style tests for fill_missing and dedup behaviors
- Integration-style tests in Phase 3 to verify sequential execution order

## Design Approval
Approved by user for:
- Full Phase 3 scope
- Transform order based on YAML array
- Fill missing strategies (default, drop_row, forward_fill, mean)
- Dedup default keep=first
- Field map: rename + drop
