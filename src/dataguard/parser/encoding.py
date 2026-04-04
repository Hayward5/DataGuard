import chardet


def detect_encoding(file_path: str) -> str:
    with open(file_path, "rb") as handle:
        raw = handle.read()

    detected = chardet.detect(raw).get("encoding") or "utf-8"
    return detected
