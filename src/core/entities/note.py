from dataclasses import dataclass, field


@dataclass
class Note:
    pitch: int = field()
    duration: float = field()
    start: float = field()
    end: float = field(init=False)

    def __post_init__(self):
        self.end = self.start + self.duration
