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
