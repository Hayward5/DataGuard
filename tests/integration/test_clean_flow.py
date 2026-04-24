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
    assert report_path.exists()

    payload = json.loads(report_path.read_text(encoding="utf-8"))
    assert payload["summary"]["error_count"] == 0
