import json

from dataguard.parser.base import BaseParser, ParseResult


class JsonParser(BaseParser):
    def parse(self, file_path: str, encoding: str | None = None) -> ParseResult:
        file_encoding = encoding or "utf-8"

        with open(file_path, encoding=file_encoding) as handle:
            content = handle.read().strip()

        if content.lstrip().startswith("{") and "\n" in content:
            records = [json.loads(line) for line in content.splitlines() if line.strip()]
            return ParseResult(records=records, errors=[], metadata={})

        data = json.loads(content)
        return ParseResult(records=data, errors=[], metadata={})
