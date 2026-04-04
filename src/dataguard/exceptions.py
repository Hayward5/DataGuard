class DataGuardError(Exception):
    """Base exception for DataGuard."""


class ParseFailure(DataGuardError):
    """Raised when an input file cannot be parsed safely."""


class SchemaFailure(DataGuardError):
    """Raised when a schema file is malformed or invalid."""


class OutputFailure(DataGuardError):
    """Raised when writing output or report files fails."""
