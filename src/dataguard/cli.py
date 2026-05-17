import json
from pathlib import Path

import click

from dataguard.output import write_csv_output
from dataguard.output_factory import get_output_writer
from dataguard.exceptions import ParseFailure, SchemaFailure
from dataguard.parser.factory import get_parser
from dataguard.reporter.assemble import assemble_report
from dataguard.reporter import get_report_renderer
from dataguard.schema.engine import validate_records
from dataguard.schema.loader import load_schema
from dataguard.transformer.engine import apply_transforms
from dataguard.transformer.loader import load_transforms


@click.group()
def main():
    """DataGuard CLI."""


@main.command()
@click.option("--input", "input_path", required=True)
@click.option("--schema", "schema_path", required=True)
@click.option("--report", "report_path")
@click.option("--format", "report_format", type=click.Choice(["json", "text"]), default="json")
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

    renderer = get_report_renderer(report_format)
    rendered = renderer(report, limit=limit)

    if report_format == "json":
        Path(report_path).write_text(json.dumps(rendered, indent=2), encoding="utf-8")
    else:
        Path(report_path).write_text(rendered, encoding="utf-8")

    if report.error_count > 0:
        raise SystemExit(1)


@main.command()
@click.option("--input", "input_path", required=True)
@click.option("--schema", "schema_path", required=True)
@click.option("--transforms", "transforms_path", required=True)
@click.option("--output", "output_path", required=True)
@click.option("--report", "report_path", required=True)
@click.option("--format", "report_format", type=click.Choice(["json", "text"]), default="json")
@click.option("--limit", default=20, type=int)
def clean(input_path, schema_path, transforms_path, output_path, report_path, report_format, limit):
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

    try:
        transforms = load_transforms(transforms_path)
    except FileNotFoundError as exc:
        raise click.ClickException("Transforms file not found") from exc

    transformed_records = apply_transforms(parse_result.records, transforms)
    results = validate_records(schema, transformed_records)

    row_has_error: dict[int, bool] = {}
    for result in results:
        row_has_error.setdefault(result.row, False)
        if result.level == "ERROR":
            row_has_error[result.row] = True

    clean_records = [
        record
        for index, record in enumerate(transformed_records, start=1)
        if not row_has_error.get(index, False)
    ]

    fieldnames = list(transformed_records[0].keys()) if transformed_records else []
    write_csv_output(clean_records, output_path, fieldnames=fieldnames)

    report = assemble_report(
        source_file=input_path,
        schema_name=schema.name,
        total_rows=len(transformed_records),
        results=results,
        parse_errors=parse_result.errors,
    )

    renderer = get_report_renderer(report_format)
    rendered = renderer(report, limit=limit)

    if report_format == "json":
        Path(report_path).write_text(json.dumps(rendered, indent=2), encoding="utf-8")
    else:
        Path(report_path).write_text(rendered, encoding="utf-8")

    if report.error_count > 0:
        raise SystemExit(1)


@main.command()
@click.option("--input", "input_path", required=True)
@click.option("--output", "output_path", required=True)
def convert(input_path, output_path):
    try:
        parser = get_parser(Path(input_path))
    except ValueError as exc:
        raise click.ClickException(str(exc)) from exc

    try:
        writer = get_output_writer(Path(output_path))
    except ValueError as exc:
        raise click.ClickException(str(exc)) from exc

    try:
        parse_result = parser.parse(input_path)
    except FileNotFoundError as exc:
        raise click.ClickException("Input file not found") from exc
    except ParseFailure as exc:
        raise click.ClickException(str(exc)) from exc

    writer(parse_result.records, output_path)
