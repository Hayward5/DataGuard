def test_date_format_converts_matching_source_format():
    from dataguard.transformer.date_format import date_format

    records = [{"join_date": "2026/04/15"}]
    result = date_format(records, {
        "operation": "date_format",
        "column": "join_date",
        "source_formats": ["%Y/%m/%d"],
        "target_format": "%Y-%m-%d",
    })

    assert result[0]["join_date"] == "2026-04-15"


def test_date_format_tries_multiple_source_formats_in_order():
    from dataguard.transformer.date_format import date_format

    records = [
        {"join_date": "2026/04/15"},
        {"join_date": "04-15-2026"},
    ]
    result = date_format(records, {
        "operation": "date_format",
        "column": "join_date",
        "source_formats": ["%Y/%m/%d", "%m-%d-%Y"],
        "target_format": "%Y-%m-%d",
    })

    assert result[0]["join_date"] == "2026-04-15"
    assert result[1]["join_date"] == "2026-04-15"


def test_date_format_keeps_original_when_no_format_matches():
    from dataguard.transformer.date_format import date_format

    records = [{"join_date": "not-a-date"}]
    result = date_format(records, {
        "operation": "date_format",
        "column": "join_date",
        "source_formats": ["%Y/%m/%d", "%m-%d-%Y"],
        "target_format": "%Y-%m-%d",
    })

    assert result[0]["join_date"] == "not-a-date"


def test_date_format_skips_missing_column():
    from dataguard.transformer.date_format import date_format

    records = [{"name": "Alice"}]
    result = date_format(records, {
        "operation": "date_format",
        "column": "join_date",
        "source_formats": ["%Y/%m/%d"],
        "target_format": "%Y-%m-%d",
    })

    assert result[0] == {"name": "Alice"}


def test_date_format_does_not_mutate_original_records():
    from dataguard.transformer.date_format import date_format

    original = [{"join_date": "2026/04/15"}]
    date_format(original, {
        "operation": "date_format",
        "column": "join_date",
        "source_formats": ["%Y/%m/%d"],
        "target_format": "%Y-%m-%d",
    })

    assert original[0]["join_date"] == "2026/04/15"


def test_date_format_applied_via_engine():
    from dataguard.transformer.engine import apply_transforms

    records = [{"join_date": "2026/04/15"}]
    transforms = [{
        "operation": "date_format",
        "column": "join_date",
        "source_formats": ["%Y/%m/%d"],
        "target_format": "%Y-%m-%d",
    }]
    result = apply_transforms(records, transforms)

    assert result[0]["join_date"] == "2026-04-15"
