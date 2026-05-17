from dataguard.reporter.models import Report


def render_text_report(report: Report, limit: int = 20) -> str:
    lines = []

    lines.append("=== DataGuard Validation Report ===")
    lines.append(f"Source : {report.source_file}")
    lines.append(f"Schema : {report.schema_name}")
    lines.append(f"Time   : {report.timestamp}")
    lines.append("")

    lines.append("Summary:")
    lines.append(f"  Total rows : {report.total_rows}")
    lines.append(f"  Passed     : {report.pass_count}")
    lines.append(f"  Warnings   : {report.warning_count}")
    lines.append(f"  Errors     : {report.error_count} ({report.parse_error_count} parse, {report.validation_error_count} validation)")
    lines.append("")

    if report.parse_errors:
        lines.append(f"Parse Errors ({report.parse_error_count}):")
        for error in report.parse_errors:
            lines.append(f"  Row {error.row}: {error.message}")
        lines.append("")

    error_details = [d for d in report.details[:limit] if d.level == "ERROR"]
    if error_details:
        lines.append(f"Validation Errors ({len(error_details)} shown, limit={limit}):")
        for detail in error_details:
            lines.append(f"  Row {detail.row}, column '{detail.column}': {detail.code} - {detail.message}")
        lines.append("")

    return "\n".join(lines)
