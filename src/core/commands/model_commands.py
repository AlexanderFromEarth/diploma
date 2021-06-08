from typing import Iterable, TypeVar

from core.base import CommandOperation
from core.entities import Note, Tab

Input = TypeVar("Input", str, bytes, Iterable[float], Iterable[Note], covariant=True)
Output = TypeVar(
    "Output", tuple[float, Iterable[float]], Iterable[Note], Iterable[Tab], covariant=True
)
Next = TypeVar("Next", covariant=True)


class ModelCommand(CommandOperation[Input, Output, Next]):
    ...


class ReadFileCommand(ModelCommand[str, tuple[float, Iterable[float]], Next]):
    ...


class FetchSignalComman(ModelCommand[bytes, tuple[float, Iterable[float]], Next]):
    ...


class ParseNotesCommand(ModelCommand[Iterable[float], Iterable[Note], Next]):
    ...


class ConvertNotesCommand(ModelCommand[Iterable[Note], Iterable[Tab], Next]):
    ...
