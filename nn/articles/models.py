import uuid
from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import DataClassJsonMixin, dataclass_json


@dataclass_json
@dataclass
class ArticleDataSource(DataClassJsonMixin):
    hn_by: Optional[str] = None
    hn_descendants: Optional[int] = None
    hn_id: Optional[int] = None
    hn_score: Optional[int] = None


@dataclass_json
@dataclass
class Article(DataClassJsonMixin):
    id: uuid.UUID
    title: str
    description: Optional[str]
    link: str
    score: float
    created_date: str
    modified_date: str
    article_data_sources: List[ArticleDataSource]
