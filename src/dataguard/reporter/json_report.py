def render_json_report(report, limit: int = 20) -> dict:
    return {
        "summary": {
            "source_file": report.source_file,
            "schema_name": report.schema_name,
            "timestamp": report.timestamp,
            "total_rows": report.total_rows,
            "pass_count": report.pass_count,
            "warning_count": report.warning_count,
            "parse_error_count": report.parse_error_count,
            "validation_error_count": report.validation_error_count,
            "error_count": report.error_count,
        },
        "error_summary": report.error_summary,
        "parse_errors": [
            {
                "row": error.row,
                "message": error.message,
            }
            for error in report.parse_errors
        ],
        "details": [
            {
                "row": detail.row,
                "column": detail.column,
                "value": detail.value,
                "level": detail.level,
                "code": detail.code,
                "message": detail.message,
            }
            for detail in report.details[:limit]
        ],
    }
