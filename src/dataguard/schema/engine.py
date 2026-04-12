from dataguard.schema.registry import get_validator
from dataguard.schema.results import ValidationResult


def validate_records(schema, records):
    results: list[ValidationResult] = []
    column_names = {column.name for column in schema.columns}

    for row_index, record in enumerate(records, start=1):
        if schema.strict:
            for key, value in record.items():
                if key not in column_names:
                    results.append(
                        ValidationResult(
                            row=row_index,
                            column=key,
                            value=value,
                            level="ERROR",
                            code="UNKNOWN_COLUMN",
                            message="Unknown column",
                        )
                    )

        for column in schema.columns:
            value = record.get(column.name)

            if column.required and (column.name not in record or value in (None, "")):
                results.append(
                    ValidationResult(
                        row=row_index,
                        column=column.name,
                        value=value,
                        level="ERROR",
                        code="REQUIRED_MISSING",
                        message="Required field missing",
                    )
                )
                continue

            if value in (None, ""):
                results.append(
                    ValidationResult(
                        row=row_index,
                        column=column.name,
                        value=value,
                        level="PASS",
                        code="OK",
                        message="",
                    )
                )
                continue

            validator = get_validator(column)
            message = validator.validate(value)
            level = "PASS" if message.code == "OK" else "ERROR"
            results.append(
                ValidationResult(
                    row=row_index,
                    column=column.name,
                    value=value,
                    level=level,
                    code=message.code,
                    message=message.message,
                )
            )

    return results
