def test_engine_applies_registered_operations_in_order():
    from dataguard.transformer.engine import apply_transforms

    records = [{"age": "1"}, {"age": "2"}]
    transforms = [
        {"operation": "type_cast", "column": "age", "target_type": "integer"},
        {"operation": "dedup", "keys": ["age"], "keep": "first"},
    ]

    result = apply_transforms(records, transforms)

    assert result == [{"age": 1}, {"age": 2}]


def test_engine_raises_on_unsupported_operation():
    import pytest

    from dataguard.transformer.engine import apply_transforms

    records = [{"age": 20}]
    transforms = [{"operation": "unknown_operation"}]

    with pytest.raises(ValueError, match="Unsupported transform operation: unknown_operation"):
        apply_transforms(records, transforms)


def test_engine_raises_on_invalid_operation_name():
    import pytest

    from dataguard.transformer.engine import apply_transforms

    records = [{"age": 20}]
    transforms = [{"operation": "invalid_op"}]

    with pytest.raises(ValueError, match="Unsupported transform operation: invalid_op"):
        apply_transforms(records, transforms)
