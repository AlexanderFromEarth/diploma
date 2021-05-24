from collections.abc import Generator
from typing import Protocol

from core.messaging import Command, Event, Request, Response


class Interaction(Protocol):
    def __call__(self, request: Request) -> Generator[Command, Event, Response]:
        ...
