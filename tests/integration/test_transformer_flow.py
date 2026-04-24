def test_transformer_flow_applies_type_cast_fill_missing_and_dedup():
    from dataguard.transformer.engine import apply_transforms

    records = [
        {"employee_id": "EMP-001", "age": "20", "salary": ""},
        {"employee_id": "EMP-001", "age": "21", "salary": "100"},
        {"employee_id": "EMP-002", "age": "30", "salary": None},
    ]
    transforms = [
        {"operation": "type_cast", "column": "age", "target_type": "integer"},
        {"operation": "fill_missing", "column": "salary", "strategy": "default", "value": "0"},
        {"operation": "dedup", "keys": ["employee_id"], "keep": "last"},
    ]

    result = apply_transforms(records, transforms)

    assert result == [
        {"employee_id": "EMP-001", "age": 21, "salary": "100"},
        {"employee_id": "EMP-002", "age": 30, "salary": "0"},
    ]


def test_transformer_flow_rejects_unknown_operation():
    import pytest

    from dataguard.transformer.engine import apply_transforms

    with pytest.raises(ValueError, match="Unsupported transform operation"):
        apply_transforms([{"x": 1}], [{"operation": "unknown"}])
