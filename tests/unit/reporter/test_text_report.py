from dataguard.reporter.assemble import assemble_report
from dataguard.parser.base import ParseErrorItem
from dataguard.reporter.text_report import render_text_report
from dataguard.schema.results import ValidationResult


def _make_report(results=None, parse_errors=None, total_rows=1):
    return assemble_report(
        source_file="employees.csv",
        schema_name="employees",
        total_rows=total_rows,
        results=results or [],
        parse_errors=parse_errors or [],
    )


def test_text_report_contains_source_and_schema():
    report = _make_report()
    output = render_text_report(report)
    assert "employees.csv" in output
    assert "employees" in output


def test_text_report_contains_summary_counts():
    report = _make_report(
        total_rows=10,
        results=[
            ValidationResult(row=1, column="age", value="abc", level="ERROR", code="INVALID_INTEGER", message="bad integer"),
        ],
    )
    output = render_text_report(report)
    assert "10" in output
    assert "Errors" in output or "errors" in output


def test_text_report_with_no_errors_shows_clean_message():
    report = _make_report(
        total_rows=3,
        results=[
            ValidationResult(row=1, column="age", value="30", level="PASS", code="OK", message="ok"),
        ],
    )
    output = render_text_report(report)
    assert "0" in output


def test_text_report_includes_parse_error_details():
    report = _make_report(
        parse_errors=[ParseErrorItem(row=2, message="Bad JSONL line")],
    )
    output = render_text_report(report)
    assert "Bad JSONL line" in output
    assert "2" in output


def test_text_report_includes_validation_error_details():
    report = _make_report(
        results=[
            ValidationResult(row=3, column="name", value="x", level="ERROR", code="STRING_TOO_SHORT", message="too short"),
        ],
    )
    output = render_text_report(report)
    assert "name" in output
    assert "STRING_TOO_SHORT" in output
    assert "too short" in output


def test_text_report_is_string():
    report = _make_report()
    output = render_text_report(report)
    assert isinstance(output, str)
