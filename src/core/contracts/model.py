from collections.abc import Iterable
from typing import Protocol

from core.entities import Note


class Model(Protocol):
    def fetch(self, raw_signal: bytes) -> Iterable[float]:
        ...

    def parse(self, signal: Iterable[float]) -> Iterable[Note]:
        ...
