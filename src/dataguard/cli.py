import json
from pathlib import Path

import click

from dataguard.parser.factory import get_parser
from dataguard.reporter.assemble import assemble_report
from dataguard.reporter.json_report import render_json_report
from dataguard.schema.engine import validate_records
from dataguard.schema.loader import load_schema


@click.group()
def main():
    """DataGuard CLI."""


@main.command()
@click.option("--input", "input_path", required=True)
@click.option("--schema", "schema_path", required=True)
@click.option("--report", "report_path")
@click.option("--format", "report_format", type=click.Choice(["json"]), default="json")
@click.option("--limit", default=20, type=int)
def validate(input_path, schema_path, report_path, report_format, limit):
    if not report_path:
        raise click.UsageError("--report is required for output")

    parser = get_parser(Path(input_path))
    parse_result = parser.parse(input_path)
    schema = load_schema(schema_path)
    results = validate_records(schema, parse_result.records)
    report = assemble_report(
        source_file=input_path,
        schema_name=schema.name,
        total_rows=len(parse_result.records),
        results=results,
    )

    payload = render_json_report(report, limit=limit)
    Path(report_path).write_text(json.dumps(payload, indent=2), encoding="utf-8")

    if report.error_count > 0:
        raise SystemExit(1)
