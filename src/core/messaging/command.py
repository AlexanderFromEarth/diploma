from dataclasses import dataclass, field
from typing import Generic, TypeVar

T = TypeVar("T")
U = TypeVar("U")


@dataclass
class Command(Generic[T, U]):
    type: T = field()
    data: U = field()
