from dataguard.schema.validators.base import BaseValidator, ValidationMessage


class BooleanValidator(BaseValidator):
    def validate(self, value) -> ValidationMessage:
        true_values = self.schema.true_values or []
        false_values = self.schema.false_values or []

        if value in true_values or value in false_values:
            return ValidationMessage(code="OK", message="")

        return ValidationMessage(code="INVALID_BOOLEAN", message="Invalid boolean value")
