from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import DataClassJsonMixin, dataclass_json

from .articles.models import Article


@dataclass_json
@dataclass
class Results(DataClassJsonMixin):
    content: Optional[List[Article]] = None
    error: Optional[str] = None
    last: Optional[bool] = None
    number: Optional[int] = None
    size: Optional[int] = None
