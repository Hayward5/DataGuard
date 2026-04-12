from dataguard.schema.validators.boolean import BooleanValidator
from dataguard.schema.validators.enum import EnumValidator
from dataguard.schema.validators.numeric import IntegerValidator
from dataguard.schema.validators.string import StringValidator


def get_validator(column_schema):
    if column_schema.type == "string":
        return StringValidator(column_schema)
    if column_schema.type == "integer":
        return IntegerValidator(column_schema)
    if column_schema.type == "enum":
        return EnumValidator(column_schema)
    if column_schema.type == "boolean":
        return BooleanValidator(column_schema)

    raise ValueError(f"Unsupported validator type: {column_schema.type}")
