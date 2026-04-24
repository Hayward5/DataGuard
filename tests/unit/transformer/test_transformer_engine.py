def test_engine_applies_registered_operations_in_order():
    from dataguard.transformer.engine import apply_transforms

    records = [{"age": "1"}, {"age": "2"}]
    transforms = [
        {"operation": "type_cast", "column": "age", "target_type": "integer"},
        {"operation": "dedup", "keys": ["age"], "keep": "first"},
    ]

    result = apply_transforms(records, transforms)

    assert result == [{"age": 1}, {"age": 2}]
