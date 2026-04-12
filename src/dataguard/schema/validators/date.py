from datetime import datetime

from dataguard.schema.validators.base import BaseValidator, ValidationMessage


class DateValidator(BaseValidator):
    def validate(self, value) -> ValidationMessage:
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except (TypeError, ValueError):
            return ValidationMessage(code="INVALID_DATE_FORMAT", message="Invalid date format")

        return ValidationMessage(code="OK", message="")
