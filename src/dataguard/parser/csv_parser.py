import csv

from dataguard.parser.base import BaseParser, ParseErrorItem, ParseResult
from dataguard.parser.encoding import detect_encoding


class CsvParser(BaseParser):
    def parse(self, file_path: str, encoding: str | None = None) -> ParseResult:
        file_encoding = encoding or detect_encoding(file_path)

        with open(file_path, encoding=file_encoding, newline="") as handle:
            sample = handle.read(1024)
            handle.seek(0)
            try:
                dialect = csv.Sniffer().sniff(sample, delimiters=",;") if sample else csv.excel
            except csv.Error:
                dialect = csv.excel
            reader = csv.reader(handle, dialect=dialect)
            rows = list(reader)

        if not rows:
            return ParseResult(records=[], errors=[], metadata={"delimiter": dialect.delimiter})

        header = rows[0]
        records: list[dict[str, str]] = []
        errors: list[ParseErrorItem] = []

        for index, row in enumerate(rows[1:], start=2):
            if len(row) != len(header):
                errors.append(ParseErrorItem(row=index, message="Mismatched column count"))
                continue
            records.append(dict(zip(header, row)))

        return ParseResult(records=records, errors=errors, metadata={"delimiter": dialect.delimiter})
