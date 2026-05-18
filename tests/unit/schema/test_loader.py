def test_loader_parses_yaml_schema(tmp_path):
    from dataguard.schema.loader import load_schema

    schema_path = tmp_path / "schema.yaml"
    schema_path.write_text(
        """
schema:
  name: employees
  version: "1.0"
  strict: true
  columns:
    - name: employee_id
      type: string
      required: true
    - name: age
      type: integer
      required: true
      min: 18
      max: 65
""",
        encoding="utf-8",
    )

    schema = load_schema(str(schema_path))

    assert schema.name == "employees"
    assert len(schema.columns) == 2


def test_loader_rejects_enum_schema_without_values(tmp_path):
    import pytest

    from dataguard.schema.loader import load_schema

    schema_path = tmp_path / "schema.yaml"
    schema_path.write_text(
        """
schema:
  name: employees
  version: "1.0"
  strict: true
  columns:
    - name: status
      type: enum
""",
        encoding="utf-8",
    )

    with pytest.raises(Exception, match="Enum schema requires values"):
        load_schema(str(schema_path))


def test_loader_rejects_boolean_schema_without_true_or_false_values(tmp_path):
    import pytest

    from dataguard.exceptions import SchemaFailure
    from dataguard.schema.loader import load_schema

    schema_path = tmp_path / "schema.yaml"
    schema_path.write_text(
        """
schema:
  name: employees
  version: "1.0"
  strict: true
  columns:
    - name: is_active
      type: boolean
      true_values: ["true"]
""",
        encoding="utf-8",
    )

    with pytest.raises(
        SchemaFailure,
        match="Boolean schema requires true_values and false_values",
    ):
        load_schema(str(schema_path))
