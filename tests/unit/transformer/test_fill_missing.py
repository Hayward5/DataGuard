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


def test_fill_missing_forward_fill_uses_previous_non_missing_value():
    from dataguard.transformer.fill_missing import fill_missing

    records = [{"age": 20}, {"age": None}, {"age": ""}, {"age": 30}]
    result = fill_missing(
        records,
        {"column": "age", "strategy": "forward_fill"},
    )

    assert result[0]["age"] == 20
    assert result[1]["age"] == 20
    assert result[2]["age"] == 20
    assert result[3]["age"] == 30


def test_fill_missing_forward_fill_keeps_original_when_no_prior_value():
    from dataguard.transformer.fill_missing import fill_missing

    records = [{"age": None}, {"age": 20}]
    result = fill_missing(
        records,
        {"column": "age", "strategy": "forward_fill"},
    )

    assert result[0]["age"] is None
    assert result[1]["age"] == 20


def test_fill_missing_mean_fills_with_numeric_average():
    from dataguard.transformer.fill_missing import fill_missing

    records = [{"age": 10}, {"age": None}, {"age": 30}, {"age": ""}]
    result = fill_missing(
        records,
        {"column": "age", "strategy": "mean"},
    )

    assert result[0]["age"] == 10
    assert result[1]["age"] == 20.0
    assert result[2]["age"] == 30
    assert result[3]["age"] == 20.0


def test_fill_missing_mean_keeps_original_when_no_valid_numeric_values():
    from dataguard.transformer.fill_missing import fill_missing

    records = [{"age": None}, {"age": ""}]
    result = fill_missing(
        records,
        {"column": "age", "strategy": "mean"},
    )

    assert result[0]["age"] is None
    assert result[1]["age"] == ""


def test_fill_missing_raises_on_unsupported_strategy():
    import pytest

    from dataguard.transformer.fill_missing import fill_missing

    records = [{"age": 20}]

    with pytest.raises(ValueError, match="Unsupported fill_missing strategy: invalid"):
        fill_missing(records, {"column": "age", "strategy": "invalid"})


def test_fill_missing_raises_on_unsupported_strategy_backward():
    import pytest

    from dataguard.transformer.fill_missing import fill_missing

    records = [{"age": 20}]

    with pytest.raises(ValueError, match="Unsupported fill_missing strategy: backward"):
        fill_missing(records, {"column": "age", "strategy": "backward"})

