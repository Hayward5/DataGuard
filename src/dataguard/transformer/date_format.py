from datetime import datetime


def date_format(records, transform):
    column = transform["column"]
    source_formats = transform["source_formats"]
    target_format = transform["target_format"]

    result = []
    for record in records:
        new_record = dict(record)
        if column not in new_record:
            result.append(new_record)
            continue
        value = new_record[column]
        converted = False
        for fmt in source_formats:
            try:
                parsed = datetime.strptime(value, fmt)
                new_record[column] = parsed.strftime(target_format)
                converted = True
                break
            except (TypeError, ValueError):
                continue
        result.append(new_record)
    return result
