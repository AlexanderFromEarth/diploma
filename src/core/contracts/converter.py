from collections.abc import Iterable
from typing import Protocol

from core.entities import Note, Tab


class Converter(Protocol):
    def convert(self, notes: Iterable[Note]) -> Iterable[Tab]:
        ...
