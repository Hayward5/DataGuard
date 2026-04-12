import re

from dataguard.schema.validators.base import BaseValidator, ValidationMessage


class StringValidator(BaseValidator):
    def validate(self, value: str) -> ValidationMessage:
        if self.schema.min_length is not None and len(value) < self.schema.min_length:
            return ValidationMessage(code="STRING_TOO_SHORT", message="Below min length")

        if self.schema.max_length is not None and len(value) > self.schema.max_length:
            return ValidationMessage(code="STRING_TOO_LONG", message="Above max length")

        if self.schema.pattern and not re.match(self.schema.pattern, value):
            return ValidationMessage(code="PATTERN_MISMATCH", message="Pattern mismatch")

        return ValidationMessage(code="OK", message="")
