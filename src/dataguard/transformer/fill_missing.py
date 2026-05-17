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

    if strategy == "drop_row":
        return [record for record in current if record.get(column) not in (None, "")]

    if strategy == "forward_fill":
        last_valid = None
        for record in current:
            if record.get(column) not in (None, ""):
                last_valid = record[column]
            elif last_valid is not None:
                record[column] = last_valid
        return current

    if strategy == "mean":
        numeric_values = []
        for record in current:
            val = record.get(column)
            if val in (None, ""):
                continue
            try:
                numeric_values.append(float(val))
            except (TypeError, ValueError):
                pass
        if not numeric_values:
            return current
        mean_value = sum(numeric_values) / len(numeric_values)
        for record in current:
            if record.get(column) in (None, ""):
                record[column] = mean_value
        return current

    raise ValueError(f"Unsupported fill_missing strategy: {strategy}")

