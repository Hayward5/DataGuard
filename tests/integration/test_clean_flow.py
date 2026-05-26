import json
from pathlib import Path

from click.testing import CliRunner

from dataguard.cli import main


def test_clean_flow_csv_writes_clean_output_and_json_report(tmp_path):
    runner = CliRunner()
    fixture_root = Path(__file__).parent.parent / "fixtures" / "clean"
    input_path = fixture_root / "valid" / "csv_clean_valid.csv"
    schema_path = Path(__file__).parent.parent.parent / "schemas" / "employees.yaml"
    transforms_path = fixture_root / "config" / "clean_transforms.yaml"
    output_path = tmp_path / "clean.csv"
    report_path = tmp_path / "report.json"

    result = runner.invoke(
        main,
        [
            "clean",
            "--input", str(input_path),
            "--schema", str(schema_path),
            "--transforms", str(transforms_path),
            "--output", str(output_path),
            "--report", str(report_path),
            "--format", "json",
        ],
    )

    assert result.exit_code == 0, result.output
    assert output_path.exists()


def test_clean_flow_text_format_writes_text_report(tmp_path):
    runner = CliRunner()
    fixture_root = Path(__file__).parent.parent / "fixtures" / "clean"
    input_path = fixture_root / "valid" / "csv_clean_valid.csv"
    schema_path = Path(__file__).parent.parent.parent / "schemas" / "employees.yaml"
    transforms_path = fixture_root / "config" / "clean_transforms.yaml"
    output_path = tmp_path / "clean.csv"
    report_path = tmp_path / "report.txt"

    result = runner.invoke(
        main,
        [
            "clean",
            "--input", str(input_path),
            "--schema", str(schema_path),
            "--transforms", str(transforms_path),
            "--output", str(output_path),
            "--report", str(report_path),
            "--format", "text",
        ],
    )

    assert result.exit_code == 0, result.output
    assert report_path.exists()

    content = report_path.read_text(encoding="utf-8")
    assert "DataGuard" in content
    assert "employees" in content


def test_clean_flow_jsonl_input_writes_clean_csv_output(tmp_path):
    runner = CliRunner()
    fixture_root = Path(__file__).parent.parent / "fixtures" / "clean"
    input_path = fixture_root / "valid" / "jsonl_clean_valid.jsonl"
    schema_path = Path(__file__).parent.parent.parent / "schemas" / "employees.yaml"
    transforms_path = fixture_root / "config" / "clean_transforms.yaml"
    output_path = tmp_path / "clean.csv"
    report_path = tmp_path / "report.json"

    result = runner.invoke(
        main,
        [
            "clean",
            "--input", str(input_path),
            "--schema", str(schema_path),
            "--transforms", str(transforms_path),
            "--output", str(output_path),
            "--report", str(report_path),
            "--format", "json",
        ],
    )

    assert result.exit_code == 0, result.output
    assert output_path.exists()


def test_clean_flow_field_map_renames_and_drops_columns(tmp_path):
    runner = CliRunner()
    fixture_root = Path(__file__).parent.parent / "fixtures" / "clean"
    input_path = fixture_root / "valid" / "csv_field_map_valid.csv"
    schema_path = Path(__file__).parent.parent.parent / "schemas" / "employees.yaml"
    transforms_path = fixture_root / "config" / "field_map_transforms.yaml"
    output_path = tmp_path / "clean.csv"
    report_path = tmp_path / "report.json"

    result = runner.invoke(
        main,
        [
            "clean",
            "--input", str(input_path),
            "--schema", str(schema_path),
            "--transforms", str(transforms_path),
            "--output", str(output_path),
            "--report", str(report_path),
            "--format", "json",
        ],
    )

    assert result.exit_code == 0, result.output
    assert output_path.exists()

    cleaned = output_path.read_text(encoding="utf-8")
    assert "employee_id" in cleaned
    assert "emp_id" not in cleaned
    assert "notes" not in cleaned
    assert "EMP-001" in cleaned
    assert "EMP-002" in cleaned

    payload = json.loads(report_path.read_text(encoding="utf-8"))
    assert payload["summary"]["error_count"] == 0


def test_clean_flow_combined_transformers(tmp_path):
    runner = CliRunner()
    fixture_root = Path(__file__).parent.parent / "fixtures" / "clean"
    input_path = fixture_root / "valid" / "csv_transformer_full_valid.csv"
    schema_path = Path(__file__).parent.parent.parent / "schemas" / "employees.yaml"
    transforms_path = fixture_root / "config" / "transformer_full_transforms.yaml"
    output_path = tmp_path / "clean.csv"
    report_path = tmp_path / "report.json"

    result = runner.invoke(
        main,
        [
            "clean",
            "--input", str(input_path),
            "--schema", str(schema_path),
            "--transforms", str(transforms_path),
            "--output", str(output_path),
            "--report", str(report_path),
            "--format", "json",
        ],
    )

    assert result.exit_code == 0, result.output
    assert output_path.exists()

    cleaned = output_path.read_text(encoding="utf-8")
    # dedup: EMP-001 重複只留一筆
    assert cleaned.count("EMP-001") == 1
    # date_format: 日期格式統一
    assert "2026-04-12" in cleaned
    assert "2026-04-10" in cleaned
    assert "2026/04/12" not in cleaned
    assert "04-10-2026" not in cleaned

    payload = json.loads(report_path.read_text(encoding="utf-8"))
    assert payload["summary"]["error_count"] == 0


def test_clean_flow_json_valid_input_writes_clean_output(tmp_path):
    runner = CliRunner()
    fixture_root = Path(__file__).parent.parent / "fixtures" / "clean"
    input_path = fixture_root / "valid" / "json_clean_valid.json"
    schema_path = Path(__file__).parent.parent.parent / "schemas" / "employees.yaml"
    transforms_path = fixture_root / "config" / "clean_transforms.yaml"
    output_path = tmp_path / "clean.csv"
    report_path = tmp_path / "report.json"

    result = runner.invoke(
        main,
        [
            "clean",
            "--input", str(input_path),
            "--schema", str(schema_path),
            "--transforms", str(transforms_path),
            "--output", str(output_path),
            "--report", str(report_path),
        ],
    )

    assert result.exit_code == 0, result.output
    assert output_path.exists()
    payload = json.loads(report_path.read_text(encoding="utf-8"))
    assert payload["summary"]["error_count"] == 0


def test_clean_flow_json_invalid_input_filters_rows_and_exits_1(tmp_path):
    runner = CliRunner()
    fixture_root = Path(__file__).parent.parent / "fixtures" / "clean"
    input_path = fixture_root / "invalid" / "json_clean_invalid.json"
    schema_path = Path(__file__).parent.parent.parent / "schemas" / "employees.yaml"
    transforms_path = fixture_root / "config" / "clean_transforms.yaml"
    output_path = tmp_path / "clean.csv"
    report_path = tmp_path / "report.json"

    result = runner.invoke(
        main,
        [
            "clean",
            "--input", str(input_path),
            "--schema", str(schema_path),
            "--transforms", str(transforms_path),
            "--output", str(output_path),
            "--report", str(report_path),
        ],
    )

    assert result.exit_code == 1, result.output
    cleaned = output_path.read_text(encoding="utf-8")
    assert "EMP-001" in cleaned
    assert "EMP-002" not in cleaned


def test_clean_flow_csv_invalid_input_filters_rows_and_exits_1(tmp_path):
    runner = CliRunner()
    fixture_root = Path(__file__).parent.parent / "fixtures" / "clean"
    input_path = fixture_root / "invalid" / "csv_clean_invalid.csv"
    schema_path = Path(__file__).parent.parent.parent / "schemas" / "employees.yaml"
    transforms_path = fixture_root / "config" / "clean_transforms.yaml"
    output_path = tmp_path / "clean.csv"
    report_path = tmp_path / "report.json"

    result = runner.invoke(
        main,
        [
            "clean",
            "--input", str(input_path),
            "--schema", str(schema_path),
            "--transforms", str(transforms_path),
            "--output", str(output_path),
            "--report", str(report_path),
        ],
    )

    assert result.exit_code == 1, result.output
    assert output_path.exists()
    assert report_path.exists()

    cleaned = output_path.read_text(encoding="utf-8")
    assert "EMP-001" in cleaned
    assert "EMP-002" not in cleaned

    payload = json.loads(report_path.read_text(encoding="utf-8"))
    assert payload["summary"]["error_count"] > 0


def test_clean_flow_jsonl_invalid_input_filters_rows_and_exits_1(tmp_path):
    runner = CliRunner()
    fixture_root = Path(__file__).parent.parent / "fixtures" / "clean"
    input_path = fixture_root / "invalid" / "jsonl_clean_invalid.jsonl"
    schema_path = Path(__file__).parent.parent.parent / "schemas" / "employees.yaml"
    transforms_path = fixture_root / "config" / "clean_transforms.yaml"
    output_path = tmp_path / "clean.csv"
    report_path = tmp_path / "report.json"

    result = runner.invoke(
        main,
        [
            "clean",
            "--input", str(input_path),
            "--schema", str(schema_path),
            "--transforms", str(transforms_path),
            "--output", str(output_path),
            "--report", str(report_path),
        ],
    )

    assert result.exit_code == 1, result.output
    cleaned = output_path.read_text(encoding="utf-8")
    assert "EMP-001" in cleaned
    assert "EMP-002" not in cleaned


def test_clean_flow_output_json_format(tmp_path):
    runner = CliRunner()
    fixture_root = Path(__file__).parent.parent / "fixtures" / "clean"
    input_path = fixture_root / "valid" / "csv_clean_valid.csv"
    schema_path = Path(__file__).parent.parent.parent / "schemas" / "employees.yaml"
    transforms_path = fixture_root / "config" / "clean_transforms.yaml"
    output_path = tmp_path / "clean.json"
    report_path = tmp_path / "report.json"

    result = runner.invoke(
        main,
        [
            "clean",
            "--input", str(input_path),
            "--schema", str(schema_path),
            "--transforms", str(transforms_path),
            "--output", str(output_path),
            "--report", str(report_path),
        ],
    )

    assert result.exit_code == 0, result.output
    assert output_path.exists()

    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert isinstance(payload, list)
    assert payload[0]["employee_id"] == "EMP-001"


def test_clean_flow_output_jsonl_format(tmp_path):
    runner = CliRunner()
    fixture_root = Path(__file__).parent.parent / "fixtures" / "clean"
    input_path = fixture_root / "valid" / "csv_clean_valid.csv"
    schema_path = Path(__file__).parent.parent.parent / "schemas" / "employees.yaml"
    transforms_path = fixture_root / "config" / "clean_transforms.yaml"
    output_path = tmp_path / "clean.jsonl"
    report_path = tmp_path / "report.json"

    result = runner.invoke(
        main,
        [
            "clean",
            "--input", str(input_path),
            "--schema", str(schema_path),
            "--transforms", str(transforms_path),
            "--output", str(output_path),
            "--report", str(report_path),
        ],
    )

    assert result.exit_code == 0, result.output
    assert output_path.exists()

    lines = output_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) >= 1
    assert json.loads(lines[0])["employee_id"] == "EMP-001"


def test_clean_flow_empty_csv_exits_0_and_writes_empty_output(tmp_path):
    runner = CliRunner()
    fixture_root = Path(__file__).parent.parent / "fixtures" / "clean"
    input_path = fixture_root / "edge" / "csv_clean_edge_empty.csv"
    schema_path = Path(__file__).parent.parent.parent / "schemas" / "employees.yaml"
    transforms_path = fixture_root / "config" / "clean_transforms.yaml"
    output_path = tmp_path / "clean.csv"
    report_path = tmp_path / "report.json"

    result = runner.invoke(
        main,
        [
            "clean",
            "--input", str(input_path),
            "--schema", str(schema_path),
            "--transforms", str(transforms_path),
            "--output", str(output_path),
            "--report", str(report_path),
        ],
    )

    assert result.exit_code == 0, result.output
    assert output_path.exists()

    payload = json.loads(report_path.read_text(encoding="utf-8"))
    assert payload["summary"]["total_rows"] == 0
    assert payload["summary"]["error_count"] == 0


def test_clean_flow_empty_json_exits_0_and_writes_empty_output(tmp_path):
    runner = CliRunner()
    fixture_root = Path(__file__).parent.parent / "fixtures" / "clean"
    input_path = fixture_root / "edge" / "json_clean_edge_empty.json"
    schema_path = Path(__file__).parent.parent.parent / "schemas" / "employees.yaml"
    transforms_path = fixture_root / "config" / "clean_transforms.yaml"
    output_path = tmp_path / "clean.csv"
    report_path = tmp_path / "report.json"

    result = runner.invoke(
        main,
        [
            "clean",
            "--input", str(input_path),
            "--schema", str(schema_path),
            "--transforms", str(transforms_path),
            "--output", str(output_path),
            "--report", str(report_path),
        ],
    )

    assert result.exit_code == 0, result.output
    assert output_path.exists()

    payload = json.loads(report_path.read_text(encoding="utf-8"))
    assert payload["summary"]["total_rows"] == 0
    assert payload["summary"]["error_count"] == 0


def test_clean_flow_empty_jsonl_exits_0_and_writes_empty_output(tmp_path):
    runner = CliRunner()
    fixture_root = Path(__file__).parent.parent / "fixtures" / "clean"
    input_path = fixture_root / "edge" / "jsonl_clean_edge_empty.jsonl"
    schema_path = Path(__file__).parent.parent.parent / "schemas" / "employees.yaml"
    transforms_path = fixture_root / "config" / "clean_transforms.yaml"
    output_path = tmp_path / "clean.csv"
    report_path = tmp_path / "report.json"

    result = runner.invoke(
        main,
        [
            "clean",
            "--input", str(input_path),
            "--schema", str(schema_path),
            "--transforms", str(transforms_path),
            "--output", str(output_path),
            "--report", str(report_path),
        ],
    )

    assert result.exit_code == 0, result.output
    assert output_path.exists()

    payload = json.loads(report_path.read_text(encoding="utf-8"))
    assert payload["summary"]["total_rows"] == 0
    assert payload["summary"]["error_count"] == 0
