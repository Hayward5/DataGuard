def test_validation_result_fields():
    from dataguard.schema.results import ValidationResult

    result = ValidationResult(
        row=1,
        column="age",
        value=20,
        level="PASS",
        code="OK",
        message="",
    )

    assert result.row == 1
    assert result.column == "age"
    assert result.value == 20
    assert result.level == "PASS"
    assert result.code == "OK"
