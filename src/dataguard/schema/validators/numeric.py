from dataguard.schema.validators.base import BaseValidator, ValidationMessage


class IntegerValidator(BaseValidator):
    def validate(self, value) -> ValidationMessage:
        try:
            parsed = int(value)
        except (TypeError, ValueError):
            return ValidationMessage(code="INVALID_INTEGER", message="Invalid integer")

        if self.schema.min is not None and parsed < self.schema.min:
            return ValidationMessage(code="OUT_OF_RANGE", message="Below min")
        if self.schema.max is not None and parsed > self.schema.max:
            return ValidationMessage(code="OUT_OF_RANGE", message="Above max")

        return ValidationMessage(code="OK", message="")
