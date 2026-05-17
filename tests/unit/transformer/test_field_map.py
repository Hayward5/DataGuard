def test_field_map_renames_single_column():
    from dataguard.transformer.field_map import field_map

    records = [{"emp_id": "E001", "name": "Alice"}]
    result = field_map(records, {"operation": "field_map", "rename": {"emp_id": "employee_id"}})

    assert result[0]["employee_id"] == "E001"
    assert "emp_id" not in result[0]
    assert result[0]["name"] == "Alice"


def test_field_map_renames_multiple_columns():
    from dataguard.transformer.field_map import field_map

    records = [{"emp_id": "E001", "dept": "Engineering"}]
    result = field_map(records, {"operation": "field_map", "rename": {"emp_id": "employee_id", "dept": "department"}})

    assert result[0]["employee_id"] == "E001"
    assert result[0]["department"] == "Engineering"
    assert "emp_id" not in result[0]
    assert "dept" not in result[0]


def test_field_map_drops_single_column():
    from dataguard.transformer.field_map import field_map

    records = [{"employee_id": "E001", "name": "Alice", "internal_notes": "secret"}]
    result = field_map(records, {"operation": "field_map", "drop": ["internal_notes"]})

    assert "internal_notes" not in result[0]
    assert result[0]["employee_id"] == "E001"
    assert result[0]["name"] == "Alice"


def test_field_map_drops_multiple_columns():
    from dataguard.transformer.field_map import field_map

    records = [{"employee_id": "E001", "name": "Alice", "notes": "x", "raw": "y"}]
    result = field_map(records, {"operation": "field_map", "drop": ["notes", "raw"]})

    assert "notes" not in result[0]
    assert "raw" not in result[0]
    assert result[0]["employee_id"] == "E001"


def test_field_map_rename_and_drop_together():
    from dataguard.transformer.field_map import field_map

    records = [{"emp_id": "E001", "name": "Alice", "internal_notes": "secret"}]
    result = field_map(
        records,
        {"operation": "field_map", "rename": {"emp_id": "employee_id"}, "drop": ["internal_notes"]},
    )

    assert result[0]["employee_id"] == "E001"
    assert result[0]["name"] == "Alice"
    assert "emp_id" not in result[0]
    assert "internal_notes" not in result[0]


def test_field_map_ignores_missing_rename_source():
    from dataguard.transformer.field_map import field_map

    records = [{"name": "Alice"}]
    result = field_map(records, {"operation": "field_map", "rename": {"emp_id": "employee_id"}})

    assert result[0] == {"name": "Alice"}


def test_field_map_ignores_missing_drop_column():
    from dataguard.transformer.field_map import field_map

    records = [{"employee_id": "E001"}]
    result = field_map(records, {"operation": "field_map", "drop": ["nonexistent"]})

    assert result[0] == {"employee_id": "E001"}


def test_field_map_does_not_mutate_original_records():
    from dataguard.transformer.field_map import field_map

    original = [{"emp_id": "E001", "name": "Alice"}]
    field_map(original, {"operation": "field_map", "rename": {"emp_id": "employee_id"}})

    assert "emp_id" in original[0]


def test_field_map_applied_via_engine():
    from dataguard.transformer.engine import apply_transforms

    records = [{"emp_id": "E001", "name": "Alice", "notes": "x"}]
    transforms = [
        {"operation": "field_map", "rename": {"emp_id": "employee_id"}, "drop": ["notes"]},
    ]
    result = apply_transforms(records, transforms)

    assert result[0]["employee_id"] == "E001"
    assert result[0]["name"] == "Alice"
    assert "emp_id" not in result[0]
    assert "notes" not in result[0]
