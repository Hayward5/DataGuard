def dedup(records, transform):
    keys = transform["keys"]
    keep = transform.get("keep", "first")

    if keep == "first":
        seen = set()
        result = []
        for record in records:
            key = tuple(record.get(field) for field in keys)
            if key in seen:
                continue
            seen.add(key)
            result.append(dict(record))
        return result

    if keep == "last":
        latest = {}
        order = []
        for record in records:
            key = tuple(record.get(field) for field in keys)
            if key not in latest:
                order.append(key)
            latest[key] = dict(record)
        return [latest[key] for key in order]

    if keep == "none":
        from collections import Counter
        key_counts = Counter(
            tuple(record.get(field) for field in keys) for record in records
        )
        return [
            dict(record)
            for record in records
            if key_counts[tuple(record.get(field) for field in keys)] == 1
        ]

    raise ValueError(f"Unsupported dedup keep mode: {keep}")
