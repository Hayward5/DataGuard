import json
from pathlib import Path

import click

from dataguard.exceptions import ParseFailure, SchemaFailure
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

    try:
        parser = get_parser(Path(input_path))
    except ValueError as exc:
        raise click.ClickException(str(exc)) from exc

    try:
        parse_result = parser.parse(input_path)
    except FileNotFoundError as exc:
        raise click.ClickException("Input file not found") from exc
    except ParseFailure as exc:
        raise click.ClickException(str(exc)) from exc

    try:
        schema = load_schema(schema_path)
    except FileNotFoundError as exc:
        raise click.ClickException("Schema file not found") from exc
    except SchemaFailure as exc:
        raise click.ClickException(str(exc)) from exc

    results = validate_records(schema, parse_result.records)
    report = assemble_report(
        source_file=input_path,
        schema_name=schema.name,
        total_rows=len(parse_result.records),
        results=results,
        parse_errors=parse_result.errors,
    )

    payload = render_json_report(report, limit=limit)
    Path(report_path).write_text(json.dumps(payload, indent=2), encoding="utf-8")

    if report.error_count > 0:
        raise SystemExit(1)


@main.command()
@click.option("--input", "input_path", required=True)
@click.option("--schema", "schema_path", required=True)
@click.option("--transforms", "transforms_path", required=True)
@click.option("--output", "output_path", required=True)
@click.option("--report", "report_path", required=True)
@click.option("--format", "report_format", type=click.Choice(["json"]), default="json")
@click.option("--limit", default=20, type=int)
def clean(input_path, schema_path, transforms_path, output_path, report_path, report_format, limit):
    raise NotImplementedError
