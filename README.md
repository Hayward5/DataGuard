# DataGuard Rebuild

DataGuard Rebuild is a schema-driven command-line tool for structured data validation, cleaning, and format conversion workflows.

The project is designed for datasets such as CSV, JSON, and JSONL, where records need to be checked against explicit rules, reported in a consistent format, cleaned through reusable transformation steps, or converted between supported structured-data formats.

## What This Repository Is Building

This repository aims to provide a reusable data quality pipeline with these core capabilities:

- validate structured records against a YAML schema
- detect and report field-level validation errors
- handle parser-level errors alongside validation results
- apply ordered data transformations through a standalone transformer layer
- clean records by applying transforms, validating the result, and writing valid rows
- convert records between CSV, JSON, and JSONL without validation or transformation

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
- `output`
  writes normalized records as CSV, JSON, or JSONL
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

## Reserved Validation Features

The schema model keeps `case_sensitive` for possible future enum or string matching behavior, but the current validators do not use it. Validation remains case-sensitive, and this behavior is intentionally left unchanged for now.

Reports keep a `warning_count` field and the internal result model keeps the `WARNING` level for compatibility with earlier report designs. Current validators do not emit warnings, so `warning_count` is expected to stay `0`; this feature is reserved and intentionally not implemented.

## Cleaning and Transformation

The repository includes a transformer layer for ordered record transformations.
This layer is intentionally isolated from file I/O so it can be tested independently and reused by CLI workflows.

Current transformer operations include:

- `type_cast`
- `fill_missing`
- `dedup`

The `clean` command uses this transformer layer, validates the transformed records against a schema, writes valid records to a CSV output file, and writes a JSON validation report.

## Format Conversion

The `convert` command performs pure structured-data format conversion across CSV, JSON, and JSONL.
It parses records from the input file based on its extension and writes records using the output file extension.

`convert` does not load a schema, apply transforms, filter rows, or emit a validation report.

## CLI Usage

Validate records and write a JSON report:

```bash
dataguard validate \
  --input tests/fixtures/validate/valid/csv_employees_valid.csv \
  --schema schemas/employees.yaml \
  --report report.json
```

Clean records with a transform config, then write clean rows and a report:

```bash
dataguard clean \
  --input tests/fixtures/clean/valid/csv_clean_valid.csv \
  --schema schemas/employees.yaml \
  --transforms tests/fixtures/clean/config/clean_transforms.yaml \
  --output clean.csv \
  --report clean-report.json
```

Convert between supported formats:

```bash
dataguard convert \
  --input tests/fixtures/convert/valid/csv_convert_valid.csv \
  --output converted.json
```

## Development

Install dependencies:

```bash
uv sync --extra dev
```

Run the test suite:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run pytest -q
```

## Contributing

We follow a standard GitHub workflow:

1. Create an issue describing the change
2. Create a branch named `issue-<number>-<description>`
3. Make changes and write tests
4. Open a PR against `main`
5. CI must pass before merge
