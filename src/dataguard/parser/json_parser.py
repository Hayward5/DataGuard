import json

from dataguard.parser.base import BaseParser, ParseResult


class JsonParser(BaseParser):
    def parse(self, file_path: str, encoding: str | None = None) -> ParseResult:
        file_encoding = encoding or "utf-8"

        with open(file_path, encoding=file_encoding) as handle:
            data = json.load(handle)

        return ParseResult(records=data, errors=[], metadata={})
