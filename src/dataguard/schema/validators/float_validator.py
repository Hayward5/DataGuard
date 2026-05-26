from dataguard.schema.validators.base import BaseValidator, ValidationMessage


class FloatValidator(BaseValidator):
    def validate(self, value) -> ValidationMessage:
        try:
            parsed = float(value)
        except (TypeError, ValueError):
            return ValidationMessage(code="INVALID_FLOAT", message="Invalid float")

        if self.schema.min is not None and parsed < self.schema.min:
            return ValidationMessage(code="OUT_OF_RANGE", message="Below min")
        if self.schema.max is not None and parsed > self.schema.max:
            return ValidationMessage(code="OUT_OF_RANGE", message="Above max")

        return ValidationMessage(code="OK", message="")
