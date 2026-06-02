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


def test_loader_raises_schema_failure_on_invalid_yaml(tmp_path):
    import pytest

    from dataguard.exceptions import SchemaFailure
    from dataguard.schema.loader import load_schema

    schema_path = tmp_path / "bad.yaml"
    schema_path.write_text("{ invalid yaml: syntax: error", encoding="utf-8")

    with pytest.raises(SchemaFailure, match="Invalid schema YAML"):
        load_schema(str(schema_path))


def test_loader_raises_schema_failure_on_non_dict_schema(tmp_path):
    import pytest

    from dataguard.exceptions import SchemaFailure
    from dataguard.schema.loader import load_schema

    schema_path = tmp_path / "array_schema.yaml"
    schema_path.write_text(
        """
schema:
  - name: employees
    version: "1.0"
""",
        encoding="utf-8",
    )

    with pytest.raises(SchemaFailure, match="Schema file must contain a schema mapping"):
        load_schema(str(schema_path))


def test_loader_raises_schema_failure_on_non_list_columns(tmp_path):
    import pytest

    from dataguard.exceptions import SchemaFailure
    from dataguard.schema.loader import load_schema

    schema_path = tmp_path / "non_list_columns.yaml"
    schema_path.write_text(
        """
schema:
  name: employees
  version: "1.0"
  columns:
    name: employee_id
    type: string
""",
        encoding="utf-8",
    )

    with pytest.raises(SchemaFailure, match="Schema columns must be a list"):
        load_schema(str(schema_path))


def test_loader_raises_schema_failure_on_unsupported_format(tmp_path):
    import pytest

    from dataguard.exceptions import SchemaFailure
    from dataguard.schema.loader import load_schema

    schema_path = tmp_path / "unsupported_format.yaml"
    schema_path.write_text(
        """
schema:
  name: employees
  version: "1.0"
  columns:
    - name: joined_at
      type: string
      format: avatar
""",
        encoding="utf-8",
    )

    with pytest.raises(SchemaFailure, match="Unsupported format: avatar"):
        load_schema(str(schema_path))
