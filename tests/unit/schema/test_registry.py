def test_registry_returns_string_integer_enum_boolean_float_and_date_validators():
    from dataguard.schema.models import ColumnSchema
    from dataguard.schema.registry import get_validator
    from dataguard.schema.validators.boolean import BooleanValidator
    from dataguard.schema.validators.date import DateValidator
    from dataguard.schema.validators.enum import EnumValidator
    from dataguard.schema.validators.float_validator import FloatValidator
    from dataguard.schema.validators.numeric import IntegerValidator
    from dataguard.schema.validators.string import StringValidator

    assert isinstance(
        get_validator(ColumnSchema(name="name", type="string")),
        StringValidator,
    )
    assert isinstance(
        get_validator(ColumnSchema(name="age", type="integer")),
        IntegerValidator,
    )
    assert isinstance(
        get_validator(ColumnSchema(name="status", type="enum", values=["ACTIVE"])),
        EnumValidator,
    )
    assert isinstance(
        get_validator(
            ColumnSchema(
                name="is_active",
                type="boolean",
                true_values=["true"],
                false_values=["false"],
            )
        ),
        BooleanValidator,
    )
    assert isinstance(
        get_validator(ColumnSchema(name="score", type="float")),
        FloatValidator,
    )
    assert isinstance(
        get_validator(ColumnSchema(name="join_date", type="string", format="date")),
        DateValidator,
    )


def test_registry_rejects_unknown_validator_type():
    import pytest

    from dataguard.schema.models import ColumnSchema
    from dataguard.schema.registry import get_validator

    with pytest.raises(ValueError, match="Unsupported validator type: unknown"):
        get_validator(ColumnSchema(name="custom", type="unknown"))
