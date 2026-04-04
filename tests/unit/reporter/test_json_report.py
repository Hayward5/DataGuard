def test_render_json_report_contains_summary_and_details():
    from dataguard.reporter.assemble import assemble_report
    from dataguard.reporter.json_report import render_json_report
    from dataguard.schema.results import ValidationResult

    report = assemble_report(
        source_file="employees.csv",
        schema_name="employees",
        total_rows=1,
        results=[
            ValidationResult(
                row=1,
                column="age",
                value="abc",
                level="ERROR",
                code="INVALID_INTEGER",
                message="bad integer",
            )
        ],
    )

    payload = render_json_report(report, limit=20)

    assert payload["summary"]["total_rows"] == 1
    assert payload["summary"]["error_count"] == 1
    assert payload["details"][0]["code"] == "INVALID_INTEGER"
