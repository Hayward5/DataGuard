def test_validate_records_returns_error_for_missing_required_and_invalid_integer():
    from dataguard.schema.engine import validate_records
    from dataguard.schema.models import ColumnSchema, Schema

    schema = Schema(
        name="employees",
        version="1.0",
        strict=True,
        columns=[
            ColumnSchema(name="employee_id", type="string", required=True),
            ColumnSchema(name="age", type="integer", required=True, min=18, max=65),
        ],
    )

    results = validate_records(
        schema,
        [
            {"employee_id": "EMP-001", "age": 30},
            {"employee_id": "EMP-002", "age": "abc"},
            {"age": 20},
        ],
    )

    codes = [result.code for result in results if result.level == "ERROR"]

    assert "INVALID_INTEGER" in codes
    assert "REQUIRED_MISSING" in codes
