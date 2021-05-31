from dataclasses import dataclass, field
from typing import Any, Iterable, Protocol, TypeVar

from core.base.command import Command, CommandEnd, CommandOperation
from core.base.error import NotExpectedType
from core.base.result import Result, try_

Next = TypeVar("Next")


class Interpeter(Protocol):
    async def switch(self, command: CommandOperation[Any, Any, Next]) -> Result[Next]:
        ...


@dataclass
class ComposedInterpeter(Interpeter):
    inters: Iterable[Interpeter] = field()

    async def switch(self, command: CommandOperation[Any, Any, Next]) -> Result[Next]:
        for inter in self.inters:
            try:
                return inter.switch(command=command)
            except NotExpectedType:
                ...
        raise NotExpectedType(superclass=CommandOperation, provided=type(command))


@dataclass
class Interactor:
    interpreter: Interpeter = field()

    async def loop(self, computation: Command[Result[Next]]) -> Result[Next]:
        if isinstance(computation, CommandOperation):
            return try_(self.loop, await self.interpreter.switch(computation))
        if isinstance(computation, CommandEnd):
            return computation.result
        raise NotExpectedType(superclass=Command, provided=type(computation))
