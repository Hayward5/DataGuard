import pytest


@pytest.mark.parametrize(
    ("value", "code"),
    [
        (1.5,    "OK"),
        (0.0,    "OK"),
        (-1.5,   "OK"),
        (1,      "OK"),      # int 可轉 float
        ("3.14", "OK"),      # 字串數字可轉 float
        (0.5,    "OUT_OF_RANGE"),   # 低於 min=1.0
        (10.1,   "OUT_OF_RANGE"),   # 高於 max=10.0
        ("abc",  "INVALID_FLOAT"),
        (None,   "INVALID_FLOAT"),
        ("",     "INVALID_FLOAT"),
    ],
)
def test_float_validator_checks_boundaries(value, code):
    from dataguard.schema.models import ColumnSchema
    from dataguard.schema.validators.float import FloatValidator

    validator = FloatValidator(
        ColumnSchema(name="score", type="float", min=1.0, max=10.0)
    )
    assert validator.validate(value).code == code


def test_float_validator_no_min_max():
    from dataguard.schema.models import ColumnSchema
    from dataguard.schema.validators.float import FloatValidator

    validator = FloatValidator(ColumnSchema(name="ratio", type="float"))
    assert validator.validate("3.14").code == "OK"
    assert validator.validate("abc").code == "INVALID_FLOAT"
    assert validator.validate(42).code == "OK"   # int 也應可轉 float


def test_float_validator_boundary_values_are_valid():
    from dataguard.schema.models import ColumnSchema
    from dataguard.schema.validators.float import FloatValidator

    validator = FloatValidator(
        ColumnSchema(name="score", type="float", min=1.0, max=10.0)
    )
    assert validator.validate(1.0).code == "OK"   # 等於 min，應合法
    assert validator.validate(10.0).code == "OK"  # 等於 max，應合法
