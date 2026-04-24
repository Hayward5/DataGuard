def type_cast(records, transform):
    column = transform["column"]
    target_type = transform["target_type"]

    def cast(value):
        if target_type == "integer":
            return int(value)
        if target_type == "float":
            return float(value)
        if target_type == "string":
            return str(value)
        if target_type == "boolean":
            lowered = str(value).strip().lower()
            if lowered in {"true", "1", "yes", "y"}:
                return True
            if lowered in {"false", "0", "no", "n"}:
                return False
            raise ValueError("invalid boolean")
        raise ValueError(f"Unsupported cast target: {target_type}")

    current = [dict(record) for record in records]
    for record in current:
        if column not in record:
            continue
        try:
            record[column] = cast(record[column])
        except (TypeError, ValueError):
            pass
    return current
