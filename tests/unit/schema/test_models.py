def test_schema_models_hold_column_definitions():
    from dataguard.schema.models import ColumnSchema, Schema

    schema = Schema(
        name="employees",
        version="1.0",
        strict=True,
        columns=[
            ColumnSchema(name="age", type="integer", required=True, min=18, max=65),
        ],
    )

    assert schema.columns[0].name == "age"
    assert schema.columns[0].min == 18

