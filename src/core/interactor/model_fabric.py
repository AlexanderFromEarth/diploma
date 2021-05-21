from typing import Literal, Protocol

from core.constants import Events
from core.entities import Model
from core.messaging import Event


class ModelFabric(Protocol):
    async def make(self) -> Event[Literal[Events.MODEL_CREATED], Model]:
        ...
