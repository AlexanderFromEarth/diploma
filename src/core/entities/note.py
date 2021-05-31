from collections.abc import Iterable
from dataclasses import dataclass, field

from core.entities.tab import Tab
from core.entities.time_interval import TimeInterval


@dataclass(frozen=True)
class Note(TimeInterval):
    pitch: int = field()

    def tabs(self) -> Iterable[Tab]:
        return []

    @classmethod
    def from_tab(cls, tab: Tab) -> "Note":
        return Note(on_time=tab.on_time, off_time=tab.off_time, pitch=43) # type: ignore
        # IDK why it's says unexpected argument
