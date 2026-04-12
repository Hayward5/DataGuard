import yaml

from dataguard.exceptions import SchemaFailure
from dataguard.schema.models import ColumnSchema, Schema


def _validate_column_schema(column: dict) -> None:
    column_type = column.get("type")

    if column_type == "enum" and not column.get("values"):
        raise SchemaFailure("Enum schema requires values")

    if column_type == "boolean" and (
        not column.get("true_values") or not column.get("false_values")
    ):
        raise SchemaFailure("Boolean schema requires true_values and false_values")

    if column.get("format") not in (None, "date"):
        raise SchemaFailure(f"Unsupported format: {column.get('format')}")


def load_schema(file_path: str) -> Schema:
    try:
        with open(file_path, encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}
    except yaml.YAMLError as exc:
        raise SchemaFailure(f"Invalid schema YAML: {exc}") from exc

    raw_schema = data.get("schema", {})
    if not isinstance(raw_schema, dict):
        raise SchemaFailure("Schema file must contain a schema mapping")

    raw_columns = raw_schema.get("columns", [])
    if not isinstance(raw_columns, list):
        raise SchemaFailure("Schema columns must be a list")

    for column in raw_columns:
        _validate_column_schema(column)

    columns = [ColumnSchema(**column) for column in raw_columns]

    return Schema(
        name=raw_schema.get("name", ""),
        version=raw_schema.get("version", ""),
        strict=bool(raw_schema.get("strict", True)),
        columns=columns,
    )
