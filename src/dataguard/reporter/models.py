from dataclasses import dataclass


@dataclass
class Report:
    source_file: str
    schema_name: str
    timestamp: str
    total_rows: int
    pass_count: int
    warning_count: int
    parse_error_count: int
    validation_error_count: int
    error_count: int
    error_summary: dict[str, dict[str, int]]
    parse_errors: list
    details: list
