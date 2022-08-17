import uuid
from dataclasses import dataclass

from dataclasses_json import DataClassJsonMixin, dataclass_json


@dataclass_json
@dataclass
class DataSource(DataClassJsonMixin):
    id: uuid.UUID
    name: str
    description: str
    link: str
