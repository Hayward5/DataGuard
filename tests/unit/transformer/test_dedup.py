def test_dedup_keep_first_removes_later_duplicates():
    from dataguard.transformer.dedup import dedup

    records = [
        {"employee_id": "EMP-001", "age": 20},
        {"employee_id": "EMP-001", "age": 21},
        {"employee_id": "EMP-002", "age": 30},
    ]

    result = dedup(records, {"keys": ["employee_id"], "keep": "first"})

    assert result == [
        {"employee_id": "EMP-001", "age": 20},
        {"employee_id": "EMP-002", "age": 30},
    ]
