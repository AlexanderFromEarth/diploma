from dataclasses import dataclass, field
from typing import Optional

from core.constants import Commands
from core.interactions import Interaction
from core.interactor.model_fabric import ModelFabric
from core.messaging import Command, Event, Request, Response


@dataclass
class Interactor:
    model_fabric: ModelFabric = field()

    async def run(self, interaction_fn: Interaction, request: Request) -> Response:
        interaction = interaction_fn(request)

        async def interact(event: Optional[Event]):
            return interact(await self.switch(interaction.send(event)))

        try:
            await interact(None)
        except StopIteration as end:
            return end.value

    async def switch(self, command: Command) -> Event:
        if command.type == Commands.CREATE_MODEL:
            return await self.model_fabric.make()
