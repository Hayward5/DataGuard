def test_detect_encoding_prefers_utf8_for_utf8_text(tmp_path):
    from dataguard.parser.encoding import detect_encoding

    file_path = tmp_path / "utf8.txt"
    file_path.write_bytes("hello world with UTF-8 content: café résumé".encode("utf-8"))

    detected = detect_encoding(str(file_path))

    assert detected.lower().replace("-", "_") == "utf_8"
