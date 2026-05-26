import json
from pathlib import Path

from click.testing import CliRunner

from dataguard.cli import main


def test_validate_flow_csv_valid_fixture(tmp_path):
    runner = CliRunner()

    fixture_root = Path(__file__).parent.parent / "fixtures" / "validate" / "valid"
    input_path = fixture_root / "csv_employees_valid.csv"
    schema_path = Path(__file__).parent.parent.parent / "schemas" / "employees.yaml"
    report_path = tmp_path / "report.json"

    result = runner.invoke(
        main,
        [
            "validate",
            "--input",
            str(input_path),
            "--schema",
            str(schema_path),
            "--report",
            str(report_path),
            "--format",
            "json",
        ],
    )

    assert result.exit_code == 0, result.output
    assert report_path.exists()

    payload = json.loads(report_path.read_text(encoding="utf-8"))
    assert payload["summary"]["error_count"] == 0


def test_validate_flow_csv_invalid_fixture_reports_week8_rule_errors(tmp_path):
    runner = CliRunner()

    fixture_root = Path(__file__).parent.parent / "fixtures" / "validate" / "invalid"
    input_path = fixture_root / "csv_employees_invalid.csv"
    schema_path = Path(__file__).parent.parent.parent / "schemas" / "employees.yaml"
    report_path = tmp_path / "report.json"

    result = runner.invoke(
        main,
        [
            "validate",
            "--input",
            str(input_path),
            "--schema",
            str(schema_path),
            "--report",
            str(report_path),
            "--format",
            "json",
        ],
    )

    assert result.exit_code == 1, result.output

    payload = json.loads(report_path.read_text(encoding="utf-8"))

    assert payload["summary"]["error_count"] == 8
    assert payload["error_summary"]["name"]["STRING_TOO_SHORT"] == 1
    assert payload["error_summary"]["name"]["STRING_TOO_LONG"] == 1
    assert payload["error_summary"]["status"]["INVALID_ENUM"] == 1
    assert payload["error_summary"]["is_active"]["INVALID_BOOLEAN"] == 1
    assert payload["error_summary"]["join_date"]["INVALID_DATE_FORMAT"] == 2
    assert payload["error_summary"]["age"]["OUT_OF_RANGE"] == 1
    assert payload["error_summary"]["age"]["INVALID_INTEGER"] == 1


def test_validate_flow_json_valid_fixture(tmp_path):
    runner = CliRunner()

    fixture_root = Path(__file__).parent.parent / "fixtures" / "validate" / "valid"
    input_path = fixture_root / "json_employees_valid.json"
    schema_path = Path(__file__).parent.parent.parent / "schemas" / "employees.yaml"
    report_path = tmp_path / "report.json"

    result = runner.invoke(
        main,
        [
            "validate",
            "--input",
            str(input_path),
            "--schema",
            str(schema_path),
            "--report",
            str(report_path),
            "--format",
            "json",
        ],
    )

    assert result.exit_code == 0, result.output

    payload = json.loads(report_path.read_text(encoding="utf-8"))
    assert payload["summary"]["error_count"] == 0


def test_validate_flow_csv_non_utf8_fixture(tmp_path):
    runner = CliRunner()

    fixture_root = Path(__file__).parent.parent / "fixtures" / "validate" / "valid"
    input_path = fixture_root / "csv_employees_utf16le.csv"
    schema_path = Path(__file__).parent.parent.parent / "schemas" / "employees.yaml"
    report_path = tmp_path / "report.json"

    result = runner.invoke(
        main,
        [
            "validate",
            "--input",
            str(input_path),
            "--schema",
            str(schema_path),
            "--report",
            str(report_path),
        ],
    )

    assert result.exit_code == 0, result.output
    payload = json.loads(report_path.read_text(encoding="utf-8"))
    assert payload["summary"]["error_count"] == 0


def test_validate_flow_json_non_utf8_fixture(tmp_path):
    runner = CliRunner()

    fixture_root = Path(__file__).parent.parent / "fixtures" / "validate" / "valid"
    input_path = fixture_root / "json_employees_utf16le.json"
    schema_path = Path(__file__).parent.parent.parent / "schemas" / "employees.yaml"
    report_path = tmp_path / "report.json"

    result = runner.invoke(
        main,
        [
            "validate",
            "--input",
            str(input_path),
            "--schema",
            str(schema_path),
            "--report",
            str(report_path),
        ],
    )

    assert result.exit_code == 0, result.output
    payload = json.loads(report_path.read_text(encoding="utf-8"))
    assert payload["summary"]["error_count"] == 0


def test_validate_flow_jsonl_valid_fixture(tmp_path):
    runner = CliRunner()

    fixture_root = Path(__file__).parent.parent / "fixtures" / "validate" / "valid"
    input_path = fixture_root / "jsonl_employees_valid.jsonl"
    schema_path = Path(__file__).parent.parent.parent / "schemas" / "employees.yaml"
    report_path = tmp_path / "report.json"

    result = runner.invoke(
        main,
        [
            "validate",
            "--input",
            str(input_path),
            "--schema",
            str(schema_path),
            "--report",
            str(report_path),
            "--format",
            "json",
        ],
    )

    assert result.exit_code == 0, result.output

    payload = json.loads(report_path.read_text(encoding="utf-8"))
    assert payload["summary"]["error_count"] == 0


def test_validate_flow_limit_restricts_report_details(tmp_path):
    runner = CliRunner()

    fixture_root = Path(__file__).parent.parent / "fixtures" / "validate" / "invalid"
    input_path = fixture_root / "csv_employees_invalid.csv"
    schema_path = Path(__file__).parent.parent.parent / "schemas" / "employees.yaml"
    report_path = tmp_path / "report.json"

    result = runner.invoke(
        main,
        [
            "validate",
            "--input",
            str(input_path),
            "--schema",
            str(schema_path),
            "--report",
            str(report_path),
            "--format",
            "json",
            "--limit",
            "3",
        ],
    )

    assert result.exit_code == 1, result.output

    payload = json.loads(report_path.read_text(encoding="utf-8"))
    assert len(payload["details"]) == 3


def test_validate_flow_jsonl_reports_parse_errors_and_validation_errors_together(tmp_path):
    runner = CliRunner()

    fixture_root = Path(__file__).parent.parent / "fixtures" / "validate" / "edge"
    input_path = fixture_root / "jsonl_employees_edge_mixed.jsonl"
    schema_path = Path(__file__).parent.parent.parent / "schemas" / "employees.yaml"
    report_path = tmp_path / "report.json"

    result = runner.invoke(
        main,
        [
            "validate",
            "--input",
            str(input_path),
            "--schema",
            str(schema_path),
            "--report",
            str(report_path),
            "--format",
            "json",
        ],
    )

    assert result.exit_code == 1, result.output

    payload = json.loads(report_path.read_text(encoding="utf-8"))
    assert payload["summary"]["parse_error_count"] == 1
    assert payload["summary"]["validation_error_count"] == 5
    assert payload["summary"]["error_count"] == 6
    assert payload["error_summary"]["name"]["STRING_TOO_LONG"] == 1
    assert payload["parse_errors"][0]["row"] == 2
    assert payload["error_summary"]["status"]["INVALID_ENUM"] == 1
    assert payload["error_summary"]["is_active"]["INVALID_BOOLEAN"] == 1
    assert payload["error_summary"]["join_date"]["INVALID_DATE_FORMAT"] == 1
    assert payload["error_summary"]["age"]["INVALID_INTEGER"] == 1


def test_validate_flow_strict_schema_reports_unknown_columns(tmp_path):
    runner = CliRunner()

    fixture_root = Path(__file__).parent.parent / "fixtures" / "validate" / "edge"
    input_path = fixture_root / "csv_employees_unknown_column.csv"
    schema_path = Path(__file__).parent.parent.parent / "schemas" / "employees.yaml"
    report_path = tmp_path / "report.json"

    result = runner.invoke(
        main,
        [
            "validate",
            "--input",
            str(input_path),
            "--schema",
            str(schema_path),
            "--report",
            str(report_path),
            "--format",
            "json",
        ],
    )

    assert result.exit_code == 1, result.output

    payload = json.loads(report_path.read_text(encoding="utf-8"))
    assert payload["summary"]["validation_error_count"] == 1
    assert payload["error_summary"]["extra_note"]["UNKNOWN_COLUMN"] == 1


def test_validate_flow_text_format_writes_text_report(tmp_path):
    runner = CliRunner()

    fixture_root = Path(__file__).parent.parent / "fixtures" / "validate" / "valid"
    input_path = fixture_root / "csv_employees_valid.csv"
    schema_path = Path(__file__).parent.parent.parent / "schemas" / "employees.yaml"
    report_path = tmp_path / "report.txt"

    result = runner.invoke(
        main,
        [
            "validate",
            "--input", str(input_path),
            "--schema", str(schema_path),
            "--report", str(report_path),
            "--format", "text",
        ],
    )

    assert result.exit_code == 0, result.output
    assert report_path.exists()

    content = report_path.read_text(encoding="utf-8")
    assert "DataGuard" in content
    assert "employees" in content


def test_validate_flow_text_format_includes_errors(tmp_path):
    runner = CliRunner()

    fixture_root = Path(__file__).parent.parent / "fixtures" / "validate" / "invalid"
    input_path = fixture_root / "csv_employees_invalid.csv"
    schema_path = Path(__file__).parent.parent.parent / "schemas" / "employees.yaml"
    report_path = tmp_path / "report.txt"

    result = runner.invoke(
        main,
        [
            "validate",
            "--input", str(input_path),
            "--schema", str(schema_path),
            "--report", str(report_path),
            "--format", "text",
        ],
    )

    assert result.exit_code == 1, result.output

    content = report_path.read_text(encoding="utf-8")
    assert "Errors" in content or "errors" in content


def test_validate_flow_json_invalid_fixture_reports_errors(tmp_path):
    runner = CliRunner()

    fixture_root = Path(__file__).parent.parent / "fixtures" / "validate" / "invalid"
    input_path = fixture_root / "json_employees_invalid.json"
    schema_path = Path(__file__).parent.parent.parent / "schemas" / "employees.yaml"
    report_path = tmp_path / "report.json"

    result = runner.invoke(
        main,
        [
            "validate",
            "--input", str(input_path),
            "--schema", str(schema_path),
            "--report", str(report_path),
        ],
    )

    assert result.exit_code == 1, result.output
    payload = json.loads(report_path.read_text(encoding="utf-8"))
    assert payload["summary"]["error_count"] == 8


def test_validate_flow_jsonl_invalid_fixture_reports_errors(tmp_path):
    runner = CliRunner()

    fixture_root = Path(__file__).parent.parent / "fixtures" / "validate" / "invalid"
    input_path = fixture_root / "jsonl_employees_invalid.jsonl"
    schema_path = Path(__file__).parent.parent.parent / "schemas" / "employees.yaml"
    report_path = tmp_path / "report.json"

    result = runner.invoke(
        main,
        [
            "validate",
            "--input", str(input_path),
            "--schema", str(schema_path),
            "--report", str(report_path),
        ],
    )

    assert result.exit_code == 1, result.output
    payload = json.loads(report_path.read_text(encoding="utf-8"))
    assert payload["summary"]["error_count"] == 8


def test_validate_flow_empty_csv_returns_zero_errors(tmp_path):
    runner = CliRunner()

    fixture_root = Path(__file__).parent.parent / "fixtures" / "validate" / "edge"
    input_path = fixture_root / "csv_employees_edge_empty.csv"
    schema_path = Path(__file__).parent.parent.parent / "schemas" / "employees.yaml"
    report_path = tmp_path / "report.json"

    result = runner.invoke(
        main,
        [
            "validate",
            "--input", str(input_path),
            "--schema", str(schema_path),
            "--report", str(report_path),
        ],
    )

    assert result.exit_code == 0, result.output
    payload = json.loads(report_path.read_text(encoding="utf-8"))
    assert payload["summary"]["total_rows"] == 0
    assert payload["summary"]["error_count"] == 0


def test_validate_reports_parse_failure_when_json_root_is_object(tmp_path):
    runner = CliRunner()
    input_path = tmp_path / "bad.json"
    input_path.write_text('{"id": "EMP-001"}', encoding="utf-8")
    schema_path = Path(__file__).parent.parent.parent / "schemas" / "employees.yaml"
    report_path = tmp_path / "report.json"

    result = runner.invoke(
        main,
        [
            "validate",
            "--input", str(input_path),
            "--schema", str(schema_path),
            "--report", str(report_path),
        ],
    )

    assert result.exit_code == 1, result.output
    assert "must be an array" in result.output
