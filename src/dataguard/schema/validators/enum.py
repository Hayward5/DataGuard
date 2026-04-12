from dataguard.schema.validators.base import BaseValidator, ValidationMessage


class EnumValidator(BaseValidator):
    def validate(self, value) -> ValidationMessage:
        allowed_values = self.schema.values or []

        if value not in allowed_values:
            return ValidationMessage(code="INVALID_ENUM", message="Invalid enum value")

        return ValidationMessage(code="OK", message="")
