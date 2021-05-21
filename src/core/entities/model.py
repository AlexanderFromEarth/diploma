from collections.abc import Iterable
from typing import Protocol

from core.entities import Note


class Model(Protocol):
    def transform(self, ts: Iterable[float]) -> Iterable[Note]:
        ...
