from dataclasses import dataclass, field
from typing import TypeVar, Generic

T = TypeVar("T")


@dataclass
class Request(Generic[T]):
    valid: bool = field()
    data: T = field()
