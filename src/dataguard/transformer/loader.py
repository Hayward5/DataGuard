import yaml


def load_transforms(file_path: str) -> list[dict]:
    with open(file_path, encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    transforms = data.get("transforms", [])
    return transforms if isinstance(transforms, list) else []
