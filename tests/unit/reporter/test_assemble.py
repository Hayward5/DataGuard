def test_assemble_report_counts_error_results():
    from dataguard.reporter.assemble import assemble_report
    from dataguard.parser.base import ParseErrorItem
    from dataguard.schema.results import ValidationResult

    report = assemble_report(
        source_file="employees.csv",
        schema_name="employees",
        total_rows=2,
        parse_errors=[
            ParseErrorItem(row=3, message="Bad JSONL line"),
        ],
        results=[
            ValidationResult(
                row=1,
                column="employee_id",
                value="EMP-001",
                level="PASS",
                code="OK",
                message="",
            ),
            ValidationResult(
                row=2,
                column="age",
                value="abc",
                level="ERROR",
                code="INVALID_INTEGER",
                message="bad integer",
            ),
        ],
    )

    assert report.total_rows == 2
    assert report.error_count == 2
    assert report.parse_error_count == 1
    assert report.validation_error_count == 1
    assert report.error_summary["age"]["INVALID_INTEGER"] == 1
