# DataGuard Phase 5 Design

Date: 2026-03-08

## Goal
Build integration tests and fixtures covering validate, convert, and clean flows with CSV/JSON/JSONL and edge cases.

## Scope Decisions
- Full coverage for validate/convert/clean
- Fixtures include valid/invalid/edge cases
- Formats covered: CSV, JSON, JSONL
- Integration tests validate exit codes, outputs, and report structure

## Fixtures Structure
Directory layout:
- tests/fixtures/validate/{valid,invalid,edge}
- tests/fixtures/convert/{valid,invalid,edge}
- tests/fixtures/clean/{valid,invalid,edge}

Naming convention: <format>_<scenario>.<ext>
- csv_employees_valid.csv
- json_products_invalid.json
- jsonl_logs_edge.jsonl

## Integration Test Coverage
Validate:
- CSV/JSON/JSONL each: valid + invalid + edge

Convert:
- CSV->JSON, JSON->CSV, JSONL->CSV
- Each: valid + edge

Clean:
- CSV/JSON/JSONL each: valid + invalid

## Edge Case Coverage
- Empty files
- Missing columns
- Type errors
- Encoding issues
- JSONL invalid line

## Verification Strategy
Each integration test checks:
- Exit code
- Output file existence and expected content
- Report file structure (if produced)

## Design Approval
Approved by user for:
- Full flow coverage
- Expanded fixtures with edge cases
- CSV/JSON/JSONL coverage
- Fixtures layout and naming
