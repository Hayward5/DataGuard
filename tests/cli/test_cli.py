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
