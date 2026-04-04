def test_json_parser_reads_array(tmp_path):
    from dataguard.parser.json_parser import JsonParser

    json_path = tmp_path / "data.json"
    json_path.write_text('[{"id": 1}, {"id": 2}]', encoding="utf-8")

    result = JsonParser().parse(str(json_path))

    assert result.records == [{"id": 1}, {"id": 2}]
    assert result.errors == []


def test_json_parser_reads_jsonl(tmp_path):
    from dataguard.parser.json_parser import JsonParser

    jsonl_path = tmp_path / "data.jsonl"
    jsonl_path.write_text('{"id": 1}\n{"id": 2}\n', encoding="utf-8")

    result = JsonParser().parse(str(jsonl_path))

    assert result.records == [{"id": 1}, {"id": 2}]
    assert result.errors == []


def test_json_parser_keeps_good_jsonl_rows_and_reports_bad_lines(tmp_path):
    from dataguard.parser.json_parser import JsonParser

    jsonl_path = tmp_path / "data.jsonl"
    jsonl_path.write_text('{"id": 1}\n{bad json}\n{"id": 2}\n', encoding="utf-8")

    result = JsonParser().parse(str(jsonl_path))

    assert result.records == [{"id": 1}, {"id": 2}]
    assert len(result.errors) == 1
    assert result.errors[0].row == 2
