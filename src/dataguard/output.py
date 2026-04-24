import csv


def write_csv_output(records, output_path: str, fieldnames=None):
    columns = fieldnames or (list(records[0].keys()) if records else [])
    with open(output_path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        if records:
            writer.writerows(records)
