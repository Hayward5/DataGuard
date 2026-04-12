def test_boolean_validator_checks_true_and_false_values():
    from dataguard.schema.models import ColumnSchema
    from dataguard.schema.validators.boolean import BooleanValidator

    validator = BooleanValidator(
        ColumnSchema(
            name="is_active",
            type="boolean",
            true_values=["true", "1", "yes", "Y"],
            false_values=["false", "0", "no", "N"],
        )
    )

    assert validator.validate("true").code == "OK"
    assert validator.validate("N").code == "OK"
    assert validator.validate("maybe").code == "INVALID_BOOLEAN"
