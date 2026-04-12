def test_enum_validator_checks_allowed_values():
    from dataguard.schema.models import ColumnSchema
    from dataguard.schema.validators.enum import EnumValidator

    validator = EnumValidator(
        ColumnSchema(
            name="status",
            type="enum",
            values=["ACTIVE", "INACTIVE", "LEAVE"],
        )
    )

    assert validator.validate("ACTIVE").code == "OK"
    assert validator.validate("UNKNOWN").code == "INVALID_ENUM"
