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


def test_dedup_keep_last_preserves_latest_duplicate():
    from dataguard.transformer.dedup import dedup

    records = [
        {"employee_id": "EMP-001", "age": 20},
        {"employee_id": "EMP-001", "age": 21},
        {"employee_id": "EMP-002", "age": 30},
    ]

    result = dedup(records, {"keys": ["employee_id"], "keep": "last"})

    assert result == [
        {"employee_id": "EMP-001", "age": 21},
        {"employee_id": "EMP-002", "age": 30},
    ]


def test_dedup_keep_none_drops_all_duplicate_rows():
    from dataguard.transformer.dedup import dedup

    records = [
        {"employee_id": "EMP-001", "age": 20},
        {"employee_id": "EMP-001", "age": 21},
        {"employee_id": "EMP-002", "age": 30},
    ]

    result = dedup(records, {"keys": ["employee_id"], "keep": "none"})

    assert result == [{"employee_id": "EMP-002", "age": 30}]


def test_dedup_keep_none_returns_all_when_no_duplicates():
    from dataguard.transformer.dedup import dedup

    records = [
        {"employee_id": "EMP-001", "age": 20},
        {"employee_id": "EMP-002", "age": 30},
    ]

    result = dedup(records, {"keys": ["employee_id"], "keep": "none"})

    assert result == [
        {"employee_id": "EMP-001", "age": 20},
        {"employee_id": "EMP-002", "age": 30},
    ]


def test_dedup_raises_on_unsupported_keep_mode():
    import pytest

    from dataguard.transformer.dedup import dedup

    records = [
        {"employee_id": "EMP-001", "age": 20},
        {"employee_id": "EMP-002", "age": 30},
    ]

    with pytest.raises(ValueError, match="Unsupported dedup keep mode: middle"):
        dedup(records, {"keys": ["employee_id"], "keep": "middle"})


def test_dedup_raises_on_unsupported_keep_mode_reverse():
    import pytest

    from dataguard.transformer.dedup import dedup

    records = [
        {"employee_id": "EMP-001", "age": 20},
        {"employee_id": "EMP-002", "age": 30},
    ]

    with pytest.raises(ValueError, match="Unsupported dedup keep mode: reverse"):
        dedup(records, {"keys": ["employee_id"], "keep": "reverse"})

