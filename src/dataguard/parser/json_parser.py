import json

from dataguard.exceptions import ParseFailure
from dataguard.parser.base import BaseParser, ParseErrorItem, ParseResult


class JsonParser(BaseParser):
    def parse(self, file_path: str, encoding: str | None = None) -> ParseResult:
        file_encoding = encoding or "utf-8"

        with open(file_path, encoding=file_encoding) as handle:
            content = handle.read().strip()

        if content.lstrip().startswith("{") and "\n" in content:
            records = []
            errors = []
            for index, line in enumerate(content.splitlines(), start=1):
                if not line.strip():
                    continue
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError as exc:
                    errors.append(ParseErrorItem(row=index, message=str(exc)))
            return ParseResult(records=records, errors=errors, metadata={})

        try:
            data = json.loads(content)
        except json.JSONDecodeError as exc:
            raise ParseFailure(f"Invalid JSON input: {exc}") from exc

        return ParseResult(records=data, errors=[], metadata={})
