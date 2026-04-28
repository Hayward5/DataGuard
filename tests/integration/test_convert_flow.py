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
