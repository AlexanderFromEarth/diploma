from dataclasses import dataclass, field
from typing import Callable, Protocol, TypeVar

from core.base.error import Error, NotExpectedType

Data = TypeVar("Data", covariant=True)


class Result(Protocol[Data]):
    ...


@dataclass
class Success(Result[Data]):
    data: Data = field()


@dataclass
class Failure(Result):
    error: Error = field()


In = TypeVar("In")
Out = TypeVar("Out")


def try_(function: Callable[[In], Result[Out]], event: Result[In]) -> Result[Out]:
    if isinstance(event, Success):
        return function(event.data)
    if isinstance(event, Failure):
        return event
    raise NotExpectedType(superclass=Result, provided=type(event))
