def type_cast(records, transform):
    column = transform["column"]
    target_type = transform["target_type"]

    current = [dict(record) for record in records]
    for record in current:
        if column not in record:
            continue
        if target_type == "integer":
            record[column] = int(record[column])
    return current
