from dataguard.reporter.assemble import assemble_report
from dataguard.reporter.json_report import render_json_report
from dataguard.reporter.text_report import render_text_report
from dataguard.reporter.models import Report


def get_report_renderer(format: str):
    if format == "json":
        return render_json_report
    elif format == "text":
        return render_text_report
    else:
        raise ValueError(f"Unknown report format: {format}")


__all__ = [
    "Report",
    "assemble_report",
    "render_json_report",
    "render_text_report",
    "get_report_renderer",
]
