import re

from dataguard.schema.validators.base import BaseValidator, ValidationMessage


class StringValidator(BaseValidator):
    def validate(self, value: str) -> ValidationMessage:
        if self.schema.pattern and not re.match(self.schema.pattern, value):
            return ValidationMessage(code="PATTERN_MISMATCH", message="Pattern mismatch")

        return ValidationMessage(code="OK", message="")
