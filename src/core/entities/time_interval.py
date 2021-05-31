from dataclasses import dataclass, field, replace

from core.base import Result, Success, Failure
from core.errors import NotEqualEntitiesError


@dataclass(frozen=True)
class TimeInterval:
    on_time: float = field(compare=False)
    off_time: float = field(compare=False)
    duration: float = field(init=False, compare=False)

    def __post_init__(self):
        object.__setattr__(self, "duration", self.off_time - self.on_time)

    def __add__(self, other: "TimeInterval") -> Result["TimeInterval"]:
        if self == other:
            return Success(replace(self, off_time=self.off_time + other.duration))
        return Failure(
            NotEqualEntitiesError(entity_type=TimeInterval, first_entity=self, second_entity=other)
        )
