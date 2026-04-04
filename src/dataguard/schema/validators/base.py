from dataclasses import dataclass


@dataclass
class ValidationMessage:
    code: str
    message: str


class BaseValidator:
    def __init__(self, schema):
        self.schema = schema
