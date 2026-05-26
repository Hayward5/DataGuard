import json
from pathlib import Path

from click.testing import CliRunner

from dataguard.cli import main


def test_convert_flow_csv_to_json_writes_output(tmp_path):
    runner = CliRunner()
    fixture_root = Path(__file__).parent.parent / "fixtures" / "convert"
    input_path = fixture_root / "valid" / "csv_convert_valid.csv"
    output_path = tmp_path / "converted.json"

    result = runner.invoke(
        main,
        [
            "convert",
            "--input", str(input_path),
            "--output", str(output_path),
        ],
    )

    assert result.exit_code == 0, result.output
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload[0]["employee_id"] == "EMP-001"


def test_convert_flow_json_to_jsonl_writes_line_delimited_output(tmp_path):
    runner = CliRunner()
    fixture_root = Path(__file__).parent.parent / "fixtures" / "convert"
    input_path = fixture_root / "valid" / "json_convert_valid.json"
    output_path = tmp_path / "converted.jsonl"

    result = runner.invoke(
        main,
        [
            "convert",
            "--input", str(input_path),
            "--output", str(output_path),
        ],
    )

    assert result.exit_code == 0, result.output
    lines = output_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    assert '"employee_id": "EMP-001"' in lines[0]


def test_convert_flow_jsonl_to_csv_writes_tabular_output(tmp_path):
    runner = CliRunner()
    fixture_root = Path(__file__).parent.parent / "fixtures" / "convert"
    input_path = fixture_root / "valid" / "jsonl_convert_valid.jsonl"
    output_path = tmp_path / "converted.csv"

    result = runner.invoke(
        main,
        [
            "convert",
            "--input", str(input_path),
            "--output", str(output_path),
        ],
    )

    assert result.exit_code == 0, result.output
    content = output_path.read_text(encoding="utf-8")
    assert "employee_id" in content
    assert "EMP-001" in content


def test_convert_flow_json_to_csv_writes_csv_output(tmp_path):
    runner = CliRunner()
    fixture_root = Path(__file__).parent.parent / "fixtures" / "convert"
    input_path = fixture_root / "valid" / "json_convert_valid.json"
    output_path = tmp_path / "converted.csv"

    result = runner.invoke(
        main,
        [
            "convert",
            "--input", str(input_path),
            "--output", str(output_path),
        ],
    )

    assert result.exit_code == 0, result.output
    content = output_path.read_text(encoding="utf-8")
    assert "employee_id" in content
    assert "EMP-002" in content


def test_convert_reports_missing_input_file(tmp_path):
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "convert",
            "--input", str(tmp_path / "missing.csv"),
            "--output", str(tmp_path / "out.json"),
        ],
    )

    assert result.exit_code == 1
    assert "Input file not found" in result.output


def test_convert_reports_unsupported_output_format(tmp_path):
    runner = CliRunner()
    fixture_root = Path(__file__).parent.parent / "fixtures" / "convert"
    input_path = fixture_root / "valid" / "csv_convert_valid.csv"
    output_path = tmp_path / "out.txt"

    result = runner.invoke(
        main,
        [
            "convert",
            "--input", str(input_path),
            "--output", str(output_path),
        ],
    )

    assert result.exit_code == 1
    assert "Unsupported output format" in result.output


def test_convert_reports_unsupported_input_format(tmp_path):
    runner = CliRunner()
    input_path = tmp_path / "in.txt"
    input_path.write_text("x", encoding="utf-8")
    output_path = tmp_path / "out.json"

    result = runner.invoke(
        main,
        [
            "convert",
            "--input", str(input_path),
            "--output", str(output_path),
        ],
    )

    assert result.exit_code == 1
    assert "Unsupported input format" in result.output


def test_convert_reports_invalid_json_input(tmp_path):
    runner = CliRunner()
    input_path = tmp_path / "bad.json"
    input_path.write_text("{bad json}", encoding="utf-8")
    output_path = tmp_path / "out.csv"

    result = runner.invoke(
        main,
        [
            "convert",
            "--input", str(input_path),
            "--output", str(output_path),
        ],
    )

    assert result.exit_code == 1
    assert "Invalid JSON input" in result.output


def test_convert_flow_empty_csv_writes_empty_output(tmp_path):
    runner = CliRunner()
    fixture_root = Path(__file__).parent.parent / "fixtures" / "convert" / "edge"
    input_path = fixture_root / "csv_convert_edge_empty.csv"
    output_path = tmp_path / "converted.json"

    result = runner.invoke(
        main,
        [
            "convert",
            "--input", str(input_path),
            "--output", str(output_path),
        ],
    )

    assert result.exit_code == 0, result.output
    assert output_path.exists()
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload == []


def test_convert_flow_jsonl_bad_line_skips_invalid_and_converts_valid(tmp_path):
    runner = CliRunner()
    fixture_root = Path(__file__).parent.parent / "fixtures" / "convert" / "edge"
    input_path = fixture_root / "jsonl_convert_edge_bad_line.jsonl"
    output_path = tmp_path / "converted.csv"

    result = runner.invoke(
        main,
        [
            "convert",
            "--input", str(input_path),
            "--output", str(output_path),
        ],
    )

    assert result.exit_code == 0, result.output
    assert output_path.exists()
    content = output_path.read_text(encoding="utf-8")
    assert "EMP-001" in content


def test_convert_reports_parse_failure_when_json_root_is_object(tmp_path):
    from click.testing import CliRunner
    from dataguard.cli import main

    runner = CliRunner()
    input_path = tmp_path / "bad.json"
    input_path.write_text('{"id": "EMP-001"}', encoding="utf-8")
    output_path = tmp_path / "out.csv"

    result = runner.invoke(
        main,
        [
            "convert",
            "--input", str(input_path),
            "--output", str(output_path),
        ],
    )

    assert result.exit_code == 1
    assert "must be an array" in result.output
