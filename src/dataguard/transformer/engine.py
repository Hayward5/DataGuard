from typing import Any, Callable

Operation = Callable[[list[dict[str, Any]], dict[str, Any]], list[dict[str, Any]]]


def apply_transforms(records: list[dict[str, Any]], transforms: list[dict[str, Any]]):
    from dataguard.transformer.dedup import dedup
    from dataguard.transformer.field_map import field_map
    from dataguard.transformer.fill_missing import fill_missing
    from dataguard.transformer.type_cast import type_cast

    registry: dict[str, Operation] = {
        "type_cast": type_cast,
        "fill_missing": fill_missing,
        "dedup": dedup,
        "field_map": field_map,
    }

    current = [dict(record) for record in records]
    for transform in transforms:
        name = transform["operation"]
        if name not in registry:
            raise ValueError(f"Unsupported transform operation: {name}")
        current = registry[name](current, transform)
    return current
