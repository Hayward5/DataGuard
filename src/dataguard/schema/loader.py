import yaml

from dataguard.schema.models import ColumnSchema, Schema


def load_schema(file_path: str) -> Schema:
    with open(file_path, encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}

    raw_schema = data.get("schema", {})
    columns = [ColumnSchema(**column) for column in raw_schema.get("columns", [])]

    return Schema(
        name=raw_schema.get("name", ""),
        version=raw_schema.get("version", ""),
        strict=bool(raw_schema.get("strict", True)),
        columns=columns,
    )
