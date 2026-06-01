# DataGuard Design

Date: 2026-03-08

## Goal
Build a pure CLI tool that validates and transforms CSV/JSON data based on a YAML schema, producing structured validation results and reports, with comprehensive automated tests.

## Scope Decisions
- Project root is `DataGuard/`
- Pure CLI only (no Web UI)
- Source layout uses `src/dataguard/`
- Testing focuses on parser, schema validators, and end-to-end CLI flows

## Architecture Overview
The system is organized into five modules with a thin CLI layer:

1) parser/ — file reading and normalization to `list[dict]`
2) schema/ — schema loading and validation engine producing `ValidationResult` items
3) transformer/ — optional transformation rules applied to records
4) reporter/ — text and JSON report generation from validation results
5) cli.py — command-line interface wiring the modules together

Each module communicates via plain Python data structures and domain error objects to minimize coupling and simplify testing.

## Data Flow
1) CLI parses arguments and validates file paths
2) parser reads input file and returns `records` plus parse errors and metadata
3) schema loader reads YAML schema into data models
4) validation engine evaluates each record and produces `ValidationResult` list
5) transformer optionally mutates records based on rules
6) reporter produces text or JSON output and writes to stdout or files

## Error Handling
- Parser errors are collected and returned alongside partial results
- Schema loading errors are surfaced as clear, user-facing messages
- Validation produces PASS/WARNING/ERROR levels with codes and messages
- CLI returns exit codes: 0 success, 1 validation errors, 2 runtime errors

Current decision note: `WARNING` remains reserved for compatibility with the report model, but current validators do not emit warnings and this behavior is intentionally not being changed.

## Testing Strategy
- TDD for all new behavior (test fails first, then minimal implementation)
- Unit tests for parsers, validators, and transformation operations
- Integration tests for full flows: validate, convert, clean
- CLI tests for argument validation and exit codes
- Fixtures for valid/invalid inputs, edge cases, and special values

## Non-Goals
- Web UI or HTTP API
- Excel input (can be considered later)
- Advanced streaming or distributed processing

## Design Approval
Approved by user on:
- Architecture and directory layout
- Data flow and module responsibilities
