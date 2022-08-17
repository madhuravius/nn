from dataclasses import dataclass
from typing import List, Optional, Union

from dataclasses_json import DataClassJsonMixin, dataclass_json

from .articles.models import Article
from .sources.models import DataSource


@dataclass_json
@dataclass
class Results(DataClassJsonMixin):
    content: Optional[Union[List[Article], List[DataSource]]] = None
    error: Optional[str] = None
    last: Optional[bool] = None
    number: Optional[int] = None
    size: Optional[int] = None
