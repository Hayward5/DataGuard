def field_map(records, transform):
    rename = transform.get("rename") or {}
    drop = transform.get("drop") or []

    result = []
    for record in records:
        new_record = {}
        for key, value in record.items():
            if key in drop:
                continue
            new_key = rename.get(key, key)
            new_record[new_key] = value
        result.append(new_record)
    return result
