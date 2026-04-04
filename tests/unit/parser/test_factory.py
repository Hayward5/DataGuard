from pathlib import Path


def test_get_parser_returns_csv_parser_for_csv():
    from dataguard.parser.csv_parser import CsvParser
    from dataguard.parser.factory import get_parser

    parser = get_parser(Path("employees.csv"))

    assert isinstance(parser, CsvParser)
