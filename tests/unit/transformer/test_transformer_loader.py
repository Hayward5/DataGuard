def test_load_transforms_reads_transform_list(tmp_path):
    from dataguard.transformer.loader import load_transforms

    config_path = tmp_path / "transforms.yaml"
    config_path.write_text(
        """
transforms:
  - operation: type_cast
    column: age
    target_type: integer
  - operation: dedup
    keys: [employee_id]
    keep: last
""",
        encoding="utf-8",
    )

    transforms = load_transforms(str(config_path))

    assert transforms == [
        {"operation": "type_cast", "column": "age", "target_type": "integer"},
        {"operation": "dedup", "keys": ["employee_id"], "keep": "last"},
    ]


def test_load_transforms_returns_empty_list_when_missing_root(tmp_path):
    from dataguard.transformer.loader import load_transforms

    config_path = tmp_path / "transforms.yaml"
    config_path.write_text("{}", encoding="utf-8")

    assert load_transforms(str(config_path)) == []


def test_load_transforms_raises_file_not_found_for_missing_file(tmp_path):
    import pytest

    from dataguard.transformer.loader import load_transforms

    missing_path = tmp_path / "missing_transforms.yaml"

    with pytest.raises(FileNotFoundError):
        load_transforms(str(missing_path))
