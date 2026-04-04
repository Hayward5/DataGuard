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
