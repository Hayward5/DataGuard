from pathlib import Path

from dataguard.parser.csv_parser import CsvParser
from dataguard.parser.json_parser import JsonParser


def get_parser(file_path: Path | str):
    path = Path(file_path)
    suffix = path.suffix.lower()

    if suffix == ".csv":
        return CsvParser()
    if suffix in {".json", ".jsonl"}:
        return JsonParser()

    raise ValueError(f"Unsupported input format: {suffix}")
