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


def test_validate_records_skips_optional_empty_values():
    from dataguard.schema.engine import validate_records
    from dataguard.schema.models import ColumnSchema, Schema

    schema = Schema(
        name="employees",
        version="1.0",
        strict=True,
        columns=[
            ColumnSchema(name="status", type="enum", values=["ACTIVE", "INACTIVE"]),
            ColumnSchema(
                name="join_date",
                type="string",
                format="date",
            ),
        ],
    )

    results = validate_records(
        schema,
        [
            {"status": "", "join_date": ""},
            {},
        ],
    )

    assert [result.code for result in results] == ["OK", "OK", "OK", "OK"]


def test_validate_records_reports_required_missing_without_secondary_errors():
    from dataguard.schema.engine import validate_records
    from dataguard.schema.models import ColumnSchema, Schema

    schema = Schema(
        name="employees",
        version="1.0",
        strict=True,
        columns=[
            ColumnSchema(name="status", type="enum", required=True, values=["ACTIVE"]),
        ],
    )

    results = validate_records(schema, [{"status": ""}, {}])

    assert [result.code for result in results] == ["REQUIRED_MISSING", "REQUIRED_MISSING"]
