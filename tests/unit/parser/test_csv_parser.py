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
