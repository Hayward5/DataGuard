import pytest


@pytest.mark.parametrize(
    ("value", "code"),
    [
        (18, "OK"),
        (65, "OK"),
        (17, "OUT_OF_RANGE"),
        (66, "OUT_OF_RANGE"),
        ("abc", "INVALID_INTEGER"),
    ],
)
def test_integer_validator_checks_boundaries(value, code):
    from dataguard.schema.models import ColumnSchema
    from dataguard.schema.validators.numeric import IntegerValidator

    validator = IntegerValidator(
        ColumnSchema(name="age", type="integer", min=18, max=65)
    )

    assert validator.validate(value).code == code
