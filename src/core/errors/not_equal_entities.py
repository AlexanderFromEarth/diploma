from dataclasses import dataclass, field
from core.base import Error


@dataclass
class NotEqualEntitiesError(Error):
    entity_type: type = field()
    first_entity: object = field()
    second_entity: object = field()
