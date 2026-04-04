import csv

from dataguard.parser.base import BaseParser, ParseResult


class CsvParser(BaseParser):
    def parse(self, file_path: str, encoding: str | None = None) -> ParseResult:
        file_encoding = encoding or "utf-8"

        with open(file_path, encoding=file_encoding, newline="") as handle:
            sample = handle.read(1024)
            handle.seek(0)
            try:
                dialect = csv.Sniffer().sniff(sample, delimiters=",;") if sample else csv.excel
            except csv.Error:
                dialect = csv.excel
            reader = csv.DictReader(handle, dialect=dialect)
            records = list(reader)

        return ParseResult(records=records, metadata={"delimiter": dialect.delimiter})
