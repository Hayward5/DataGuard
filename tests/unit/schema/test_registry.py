def test_registry_returns_string_integer_and_enum_validators():
    from dataguard.schema.models import ColumnSchema
    from dataguard.schema.registry import get_validator
    from dataguard.schema.validators.enum import EnumValidator
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
