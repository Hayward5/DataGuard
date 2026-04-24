from click.testing import CliRunner

from dataguard.cli import main


def test_validate_requires_report_path():
    runner = CliRunner()

    result = runner.invoke(
        main,
        ["validate", "--input", "x.csv", "--schema", "schema.yaml"],
    )

    assert result.exit_code == 2
    assert "--report is required" in result.output


def test_validate_rejects_unsupported_input_format(tmp_path):
    runner = CliRunner()
    input_path = tmp_path / "data.txt"
    input_path.write_text("x", encoding="utf-8")
    schema_path = tmp_path / "schema.yaml"
    schema_path.write_text("schema:\n  name: test\n  version: '1.0'\n  columns: []\n", encoding="utf-8")
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

    assert result.exit_code == 1
    assert "Unsupported input format" in result.output


def test_validate_reports_missing_input_file(tmp_path):
    runner = CliRunner()
    schema_path = tmp_path / "schema.yaml"
    schema_path.write_text("schema:\n  name: test\n  version: '1.0'\n  columns: []\n", encoding="utf-8")
    report_path = tmp_path / "report.json"

    result = runner.invoke(
        main,
        [
            "validate",
            "--input",
            str(tmp_path / "missing.csv"),
            "--schema",
            str(schema_path),
            "--report",
            str(report_path),
        ],
    )

    assert result.exit_code == 1
    assert "Input file not found" in result.output


def test_validate_reports_missing_schema_file(tmp_path):
    runner = CliRunner()
    input_path = tmp_path / "employees.csv"
    input_path.write_text("employee_id,age\nEMP-001,30\n", encoding="utf-8")
    report_path = tmp_path / "report.json"

    result = runner.invoke(
        main,
        [
            "validate",
            "--input",
            str(input_path),
            "--schema",
            str(tmp_path / "missing.yaml"),
            "--report",
            str(report_path),
        ],
    )

    assert result.exit_code == 1
    assert "Schema file not found" in result.output


def test_validate_reports_invalid_schema(tmp_path):
    runner = CliRunner()
    input_path = tmp_path / "employees.csv"
    input_path.write_text("employee_id,age\nEMP-001,30\n", encoding="utf-8")
    schema_path = tmp_path / "schema.yaml"
    schema_path.write_text("schema:\n  name: test\n  version: '1.0'\n  columns:\n    - name: status\n      type: enum\n", encoding="utf-8")
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

    assert result.exit_code == 1
    assert "Enum schema requires values" in result.output


def test_validate_reports_invalid_json_input(tmp_path):
    runner = CliRunner()
    input_path = tmp_path / "employees.json"
    input_path.write_text("{bad json}", encoding="utf-8")
    schema_path = tmp_path / "schema.yaml"
    schema_path.write_text("schema:\n  name: test\n  version: '1.0'\n  columns: []\n", encoding="utf-8")
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

    assert result.exit_code == 1
    assert "Invalid JSON input" in result.output


def test_clean_requires_output_and_report_paths():
    runner = CliRunner()

    result = runner.invoke(
        main,
        ["clean", "--input", "x.csv", "--schema", "schema.yaml"],
    )

    assert result.exit_code == 2
