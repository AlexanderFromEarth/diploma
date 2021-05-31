from dataclasses import dataclass, field

from core.entities.time_interval import TimeInterval


@dataclass(frozen=True)
class Tab(TimeInterval):
    fret: int = field()
    string: int = field()
