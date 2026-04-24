# DataGuard Rebuild

DataGuard Rebuild is a schema-driven command-line tool for structured data validation, transformation, and future cleaning / conversion workflows.

The project is designed for datasets such as CSV, JSON, and JSONL, where records need to be checked against explicit rules, reported in a consistent format, and later processed through reusable transformation steps.

## What This Repository Is Building

This repository aims to provide a reusable data quality pipeline with these core capabilities:

- validate structured records against a YAML schema
- detect and report field-level validation errors
- handle parser-level errors alongside validation results
- apply ordered data transformations through a standalone transformer layer
- support future CLI flows for cleaning and conversion

## Current Core Components

The codebase is organized around a few core modules:

- `parser`
  reads CSV, JSON, and JSONL inputs and normalizes them into record lists
- `schema`
  loads YAML schema definitions and evaluates validation rules
- `reporter`
  assembles validation results and renders JSON reports
- `transformer`
  applies ordered record transformations such as type casting, missing-value handling, and deduplication
- `cli`
  connects the modules into command-line workflows

## Validation Capabilities

The validation layer currently supports schema-driven checks such as:

- required fields
- string pattern matching
- string length limits
- integer range validation
- enum validation
- boolean validation
- date format validation
- strict schema checking for unknown columns

Validation reports include both validation errors and parse errors so that malformed input and invalid field values can be reviewed together.

## Transformer Foundation

The repository also includes an initial transformer foundation for ordered record transformations.  
This layer is intentionally isolated from file I/O so it can be reused by future `clean` and `convert` flows.

Current transformer operations include:

- `type_cast`
- `fill_missing`
- `dedup`

## Development

Install dependencies:

```bash
uv sync --extra dev
```

Run the test suite:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run pytest -q
```
