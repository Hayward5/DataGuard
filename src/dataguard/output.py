import csv
import json


def write_csv_output(records, output_path: str, fieldnames=None):
    columns = fieldnames or (list(records[0].keys()) if records else [])
    with open(output_path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        if records:
            writer.writerows(records)


def write_json_output(records, output_path: str):
    with open(output_path, "w", encoding="utf-8") as handle:
        json.dump(records, handle, indent=2)


def write_jsonl_output(records, output_path: str):
    with open(output_path, "w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record))
            handle.write("\n")
