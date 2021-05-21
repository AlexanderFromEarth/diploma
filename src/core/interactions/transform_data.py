from collections.abc import Generator, Iterable
from typing import Literal

from core.constants import Commands, Events
from core.entities import Model, Note
from core.messaging import Command, Event, Request, Response


def transform_data(
    _: Request[bytes]
) -> Generator[Command[Literal[Commands.CREATE_MODEL], None], Event[
    Literal[Events.MODEL_CREATED], Model], Response[Iterable[Note]]]:
    resp = (yield {})
    return Response(True, resp, "OK")
