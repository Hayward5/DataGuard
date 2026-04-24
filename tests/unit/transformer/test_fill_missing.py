def test_fill_missing_default_replaces_none_and_empty_values():
    from dataguard.transformer.fill_missing import fill_missing

    records = [{"age": None}, {"age": ""}, {"age": 20}]
    result = fill_missing(
        records,
        {"column": "age", "strategy": "default", "value": 0},
    )

    assert result == [{"age": 0}, {"age": 0}, {"age": 20}]


def test_fill_missing_drop_row_removes_records_with_missing_values():
    from dataguard.transformer.fill_missing import fill_missing

    records = [{"age": None}, {"age": ""}, {"age": 20}]
    result = fill_missing(
        records,
        {"column": "age", "strategy": "drop_row"},
    )

    assert result == [{"age": 20}]
