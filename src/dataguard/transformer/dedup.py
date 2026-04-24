def dedup(records, transform):
    keys = transform["keys"]
    keep = transform.get("keep", "first")

    if keep != "first":
        raise ValueError(f"Unsupported dedup keep mode: {keep}")

    seen = set()
    result = []
    for record in records:
        key = tuple(record.get(field) for field in keys)
        if key in seen:
            continue
        seen.add(key)
        result.append(dict(record))
    return result
