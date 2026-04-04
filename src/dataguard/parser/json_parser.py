from dataguard.parser.base import BaseParser, ParseResult


class JsonParser(BaseParser):
    def parse(self, file_path: str, encoding: str | None = None) -> ParseResult:
        return ParseResult()
