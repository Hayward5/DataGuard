def fill_missing(records, transform):
    column = transform["column"]
    strategy = transform["strategy"]

    current = [dict(record) for record in records]

    if strategy == "default":
        default_value = transform.get("value")
        for record in current:
            if record.get(column) in (None, ""):
                record[column] = default_value
        return current

    raise ValueError(f"Unsupported fill_missing strategy: {strategy}")
