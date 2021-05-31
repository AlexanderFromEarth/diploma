from dataclasses import dataclass, field, replace
from typing import Callable, Generic, Protocol, TypeVar

from core.base.error import NotExpectedType

Input = TypeVar("Input", covariant=True)
Output = TypeVar("Output", covariant=True)
Next = TypeVar("Next", covariant=True)


class Command(Protocol[Next]):
    ...


@dataclass
class CommandOperation(Command[Next], Generic[Input, Output, Next]):
    input: Input = field()
    continuation: Callable[[Output], Command[Next]] = field()


@dataclass
class CommandEnd(Command[Next]):
    result: Next = field()


In = TypeVar("In")
Out = TypeVar("Out")


def combine(function: Callable[[In], Command[Out]], command: Command[In]) -> Command[Out]:
    if isinstance(command, CommandOperation):
        cont = command.continuation
        return replace(
            command,
            continuation=lambda output: combine(function, cont(output))  # type: ignore
        )
        # IDK why it's says too many args
    if isinstance(command, CommandEnd):
        return function(command.result)
    raise NotExpectedType(superclass=Command, provided=type(command))
