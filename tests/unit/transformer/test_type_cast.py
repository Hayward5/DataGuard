import pytest


@pytest.mark.parametrize(
    ("value", "target_type", "expected"),
    [
        ("10", "integer", 10),
        ("3.5", "float", 3.5),
        (10, "string", "10"),
        ("yes", "boolean", True),
        ("0", "boolean", False),
    ],
)
def test_type_cast_converts_supported_types(value, target_type, expected):
    from dataguard.transformer.type_cast import type_cast

    records = [{"value": value}]
    result = type_cast(records, {"column": "value", "target_type": target_type})

    assert result[0]["value"] == expected


def test_type_cast_keeps_original_value_when_conversion_fails():
    from dataguard.transformer.type_cast import type_cast

    records = [{"value": "bad"}]
    result = type_cast(records, {"column": "value", "target_type": "integer"})

    assert result[0]["value"] == "bad"
