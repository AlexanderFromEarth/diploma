from dataclasses import dataclass, field


class Error(BaseException):
    ...


@dataclass
class NotExpectedType(TypeError):
    superclass: type = field()
    provided: type = field()
