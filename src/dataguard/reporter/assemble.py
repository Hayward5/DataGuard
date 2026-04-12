from datetime import datetime, timezone

from dataguard.reporter.models import Report


def assemble_report(
    source_file: str,
    schema_name: str,
    total_rows: int,
    results: list,
    parse_errors: list | None = None,
):
    parse_errors = parse_errors or []
    pass_count = sum(1 for result in results if result.level == "PASS")
    warning_count = sum(1 for result in results if result.level == "WARNING")
    validation_error_count = sum(1 for result in results if result.level == "ERROR")
    parse_error_count = len(parse_errors)
    error_count = validation_error_count + parse_error_count

    error_summary: dict[str, dict[str, int]] = {}
    for result in results:
        if result.level != "ERROR":
            continue
        error_summary.setdefault(result.column, {})
        error_summary[result.column].setdefault(result.code, 0)
        error_summary[result.column][result.code] += 1

    return Report(
        source_file=source_file,
        schema_name=schema_name,
        timestamp=datetime.now(timezone.utc).isoformat(),
        total_rows=total_rows,
        pass_count=pass_count,
        warning_count=warning_count,
        parse_error_count=parse_error_count,
        validation_error_count=validation_error_count,
        error_count=error_count,
        error_summary=error_summary,
        parse_errors=parse_errors,
        details=results,
    )
