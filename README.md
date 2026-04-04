# DataGuard Rebuild

DataGuard Rebuild is a schema-driven CLI tool for structured data validation, conversion, and cleaning.

## Week 7 Scope

Week 7 implements:

- project scaffold
- parser MVP for CSV / JSON / JSONL
- minimal YAML schema loading
- minimal validation engine (`required`, `string`, `integer`)
- JSON validation report
- one end-to-end `validate` smoke flow

## Development

```bash
uv sync --extra dev
UV_CACHE_DIR=/tmp/uv-cache uv run pytest -q
```
