import uuid
from dataclasses import dataclass

from dataclasses_json import dataclass_json, DataClassJsonMixin


@dataclass_json
@dataclass
class DataSource(DataClassJsonMixin):
    id: uuid.UUID
    name: str
    description: str
    link: str
