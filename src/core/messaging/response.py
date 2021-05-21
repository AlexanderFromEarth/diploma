from dataclasses import dataclass, field
from typing import TypeVar, Generic

T = TypeVar("T")


@dataclass
class Response(Generic[T]):
    success: bool = field()
    data: T = field()
    message: str = field()
