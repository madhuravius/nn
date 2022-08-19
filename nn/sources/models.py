import uuid
from dataclasses import dataclass
from typing import Optional

from dataclasses_json import DataClassJsonMixin, dataclass_json


@dataclass_json
@dataclass
class DataSourceMetadata(DataClassJsonMixin):
    group_as: Optional[str] = None
    subreddit: Optional[str] = None


@dataclass_json
@dataclass
class DataSource(DataClassJsonMixin):
    id: uuid.UUID
    name: str
    description: str
    link: str
    metadata: DataSourceMetadata
