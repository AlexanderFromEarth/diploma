from typing import Iterable, TypeVar

from core.base import CommandOperation
from core.entities import Note, Tab

Input = TypeVar("Input", bytes, Iterable[float], Iterable[Note], covariant=True)
Output = TypeVar("Output", Iterable[float], Iterable[Note], Iterable[Tab], covariant=True)
Next = TypeVar("Next", covariant=True)


class ModelCommand(CommandOperation[Input, Output, Next]):
    ...


class FetchSignalComman(ModelCommand[bytes, Iterable[float], Next]):
    ...


class ParseNotesCommand(ModelCommand[Iterable[float], Iterable[Note], Next]):
    ...


class ConvertNotesCommand(ModelCommand[Iterable[Note], Iterable[Tab], Next]):
    ...
