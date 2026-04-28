from pathlib import Path


def test_get_output_writer_returns_csv_writer_for_csv_suffix():
    from dataguard.output_factory import get_output_writer

    writer = get_output_writer(Path("out.csv"))

    assert writer.__name__ == "write_csv_output"


def test_get_output_writer_returns_json_writer_for_json_suffix():
    from dataguard.output_factory import get_output_writer

    writer = get_output_writer(Path("out.json"))

    assert writer.__name__ == "write_json_output"


def test_get_output_writer_returns_jsonl_writer_for_jsonl_suffix():
    from dataguard.output_factory import get_output_writer

    writer = get_output_writer(Path("out.jsonl"))

    assert writer.__name__ == "write_jsonl_output"


def test_get_output_writer_raises_for_unsupported_suffix():
    from dataguard.output_factory import get_output_writer

    try:
        get_output_writer(Path("out.txt"))
    except ValueError as exc:
        assert "Unsupported output format" in str(exc)
    else:
        raise AssertionError("Expected ValueError for unsupported output format")
