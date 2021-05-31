from collections.abc import Iterable

from core.base import CommandEnd
from core.commands import FetchSignalComman, ModelCommand
from core.entities import Note


def fetch(raw: bytes) -> ModelCommand[Iterable[Note]]:
    return FetchSignalComman(input=raw, continuation=CommandEnd)
