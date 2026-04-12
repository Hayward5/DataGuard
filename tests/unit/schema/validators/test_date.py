def test_date_validator_checks_iso_date_format():
    from dataguard.schema.models import ColumnSchema
    from dataguard.schema.validators.date import DateValidator

    validator = DateValidator(
        ColumnSchema(
            name="join_date",
            type="string",
            format="date",
        )
    )

    assert validator.validate("2026-04-12").code == "OK"
    assert validator.validate("2026/04/12").code == "INVALID_DATE_FORMAT"
    assert validator.validate("bad-date").code == "INVALID_DATE_FORMAT"
