from pathlib import Path

import pytest


def test_get_parser_returns_csv_parser_for_csv():
    from dataguard.parser.csv_parser import CsvParser
    from dataguard.parser.factory import get_parser

    parser = get_parser(Path("employees.csv"))

    assert isinstance(parser, CsvParser)


def test_get_parser_returns_json_parser_for_json_and_jsonl():
    from dataguard.parser.factory import get_parser
    from dataguard.parser.json_parser import JsonParser

    assert isinstance(get_parser(Path("employees.json")), JsonParser)
    assert isinstance(get_parser(Path("employees.jsonl")), JsonParser)


def test_get_parser_rejects_unsupported_extension():
    from dataguard.parser.factory import get_parser

    with pytest.raises(ValueError, match="Unsupported input format"):
        get_parser(Path("employees.xlsx"))
