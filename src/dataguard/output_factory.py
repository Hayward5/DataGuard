from pathlib import Path

from dataguard.output import write_csv_output, write_json_output, write_jsonl_output


def get_output_writer(path: Path):
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return write_csv_output
    if suffix == ".json":
        return write_json_output
    if suffix == ".jsonl":
        return write_jsonl_output
    raise ValueError(f"Unsupported output format: {suffix or '<none>'}")
