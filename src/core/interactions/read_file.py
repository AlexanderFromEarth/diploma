from collections.abc import Iterable

from core.base import CommandEnd
from core.commands import ReadFileCommand, ModelCommand


def read(path: str) -> ModelCommand[tuple[float, Iterable[float]]]:
    return ReadFileCommand(input=path, continuation=CommandEnd)
