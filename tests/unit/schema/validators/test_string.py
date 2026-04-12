def test_string_validator_checks_pattern():
    from dataguard.schema.models import ColumnSchema
    from dataguard.schema.validators.string import StringValidator

    validator = StringValidator(
        ColumnSchema(
            name="employee_id",
            type="string",
            required=True,
            pattern=r"^EMP-[0-9]{3}$",
        )
    )

    assert validator.validate("EMP-123").code == "OK"
    assert validator.validate("BAD-123").code == "PATTERN_MISMATCH"


def test_string_validator_checks_min_and_max_length():
    from dataguard.schema.models import ColumnSchema
    from dataguard.schema.validators.string import StringValidator

    validator = StringValidator(
        ColumnSchema(
            name="name",
            type="string",
            min_length=3,
            max_length=5,
        )
    )

    assert validator.validate("Al").code == "STRING_TOO_SHORT"
    assert validator.validate("Alice").code == "OK"
    assert validator.validate("Robert").code == "STRING_TOO_LONG"
