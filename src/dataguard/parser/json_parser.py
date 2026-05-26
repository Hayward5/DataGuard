import json

from dataguard.exceptions import ParseFailure
from dataguard.parser.base import BaseParser, ParseErrorItem, ParseResult
from dataguard.parser.encoding import detect_encoding


class JsonParser(BaseParser):
    def parse(self, file_path: str, encoding: str | None = None) -> ParseResult:
        file_encoding = encoding or detect_encoding(file_path)

        with open(file_path, encoding=file_encoding) as handle:
            content = handle.read().strip()

        if not content:
            return ParseResult(records=[], errors=[], metadata={})

        if content.lstrip().startswith("{") and "\n" in content:
            records = []
            errors = []
            for index, line in enumerate(content.splitlines(), start=1):
                if not line.strip():
                    continue
                try:
                    item = json.loads(line)
                except json.JSONDecodeError as exc:
                    errors.append(ParseErrorItem(row=index, message=str(exc)))
                    continue
                if not isinstance(item, dict):
                    errors.append(
                        ParseErrorItem(
                            row=index,
                            message=f"Expected object, got {type(item).__name__}",
                        )
                    )
                else:
                    records.append(item)
            return ParseResult(records=records, errors=errors, metadata={})

        try:
            data = json.loads(content)
        except json.JSONDecodeError as exc:
            raise ParseFailure(f"Invalid JSON input: {exc}") from exc

        if not isinstance(data, list):
            raise ParseFailure(
                f"JSON input must be an array of objects, got {type(data).__name__}"
            )

        records = []
        errors = []
        for index, item in enumerate(data, start=1):
            if not isinstance(item, dict):
                errors.append(
                    ParseErrorItem(
                        row=index,
                        message=f"Expected object, got {type(item).__name__}",
                    )
                )
            else:
                records.append(item)

        return ParseResult(records=records, errors=errors, metadata={})
