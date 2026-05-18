def test_csv_parser_reads_header_and_rows(tmp_path):
    from dataguard.parser.csv_parser import CsvParser

    csv_path = tmp_path / "employees.csv"
    csv_path.write_text("id,name\n1,Alice\n2,Bob\n", encoding="utf-8")

    result = CsvParser().parse(str(csv_path))

    assert result.records == [
        {"id": "1", "name": "Alice"},
        {"id": "2", "name": "Bob"},
    ]
    assert result.errors == []
    assert result.metadata["delimiter"] == ","


def test_csv_parser_detects_semicolon_delimiter(tmp_path):
    from dataguard.parser.csv_parser import CsvParser

    csv_path = tmp_path / "employees.csv"
    csv_path.write_text("id;name\n1;Alice\n2;Bob\n", encoding="utf-8")

    result = CsvParser().parse(str(csv_path))

    assert result.records == [
        {"id": "1", "name": "Alice"},
        {"id": "2", "name": "Bob"},
    ]
    assert result.errors == []
    assert result.metadata["delimiter"] == ";"


def test_csv_parser_returns_empty_result_for_empty_file(tmp_path):
    from dataguard.parser.csv_parser import CsvParser

    csv_path = tmp_path / "employees.csv"
    csv_path.write_text("", encoding="utf-8")

    result = CsvParser().parse(str(csv_path))

    assert result.records == []
    assert result.errors == []
    assert result.metadata["delimiter"] == ","


def test_csv_parser_reports_mismatched_columns(tmp_path):
    from dataguard.parser.csv_parser import CsvParser

    csv_path = tmp_path / "employees.csv"
    csv_path.write_text("id,name,age\n1,Alice,30\n2,Bob\n", encoding="utf-8")

    result = CsvParser().parse(str(csv_path))

    assert result.records == [{"id": "1", "name": "Alice", "age": "30"}]
    assert len(result.errors) == 1
    assert result.errors[0].row == 3
    assert "mismatched" in result.errors[0].message.lower()
    assert result.metadata["delimiter"] == ","


def test_csv_parser_detects_non_utf8_encoding_when_not_provided(tmp_path):
    from dataguard.parser.csv_parser import CsvParser

    csv_path = tmp_path / "employees.csv"
    csv_path.write_bytes("id,name\n1,Jos\u00e9\n".encode("utf-16-le"))

    result = CsvParser().parse(str(csv_path))

    assert result.records == [{"id": "1", "name": "Jos\u00e9"}]
    assert result.errors == []


def test_csv_parser_uses_explicit_encoding_when_provided(tmp_path):
    from dataguard.parser.csv_parser import CsvParser

    csv_path = tmp_path / "employees.csv"
    csv_path.write_bytes("id,name\n1,Jos\u00e9\n".encode("utf-16-le"))

    result = CsvParser().parse(str(csv_path), encoding="utf-16-le")

    assert result.records == [{"id": "1", "name": "Jos\u00e9"}]
    assert result.errors == []
