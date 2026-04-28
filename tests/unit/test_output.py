def test_write_csv_output_writes_header_and_rows(tmp_path):
    from dataguard.output import write_csv_output

    output_path = tmp_path / "clean.csv"
    records = [
        {"employee_id": "EMP-001", "age": 20},
        {"employee_id": "EMP-002", "age": 30},
    ]

    write_csv_output(records, str(output_path))

    assert output_path.read_text(encoding="utf-8") == (
        "employee_id,age\n"
        "EMP-001,20\n"
        "EMP-002,30\n"
    )


def test_write_csv_output_writes_header_only_for_empty_records(tmp_path):
    from dataguard.output import write_csv_output

    output_path = tmp_path / "clean.csv"

    write_csv_output([], str(output_path), fieldnames=["employee_id", "age"])

    assert output_path.read_text(encoding="utf-8") == "employee_id,age\n"


def test_write_json_output_writes_array_payload(tmp_path):
    from dataguard.output import write_json_output

    output_path = tmp_path / "records.json"
    records = [{"employee_id": "EMP-001"}, {"employee_id": "EMP-002"}]

    write_json_output(records, str(output_path))

    assert output_path.read_text(encoding="utf-8") == (
        '[\n'
        '  {\n'
        '    "employee_id": "EMP-001"\n'
        '  },\n'
        '  {\n'
        '    "employee_id": "EMP-002"\n'
        '  }\n'
        "]"
    )


def test_write_jsonl_output_writes_one_object_per_line(tmp_path):
    from dataguard.output import write_jsonl_output

    output_path = tmp_path / "records.jsonl"
    records = [{"employee_id": "EMP-001"}, {"employee_id": "EMP-002"}]

    write_jsonl_output(records, str(output_path))

    lines = output_path.read_text(encoding="utf-8").splitlines()
    assert lines == [
        '{"employee_id": "EMP-001"}',
        '{"employee_id": "EMP-002"}',
    ]
