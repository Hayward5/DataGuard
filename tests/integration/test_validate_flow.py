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
