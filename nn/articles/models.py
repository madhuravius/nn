import uuid
from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class ArticleDataSource:
    hn_by: Optional[str]
    hn_descendants: Optional[int]
    hn_id: Optional[int]
    hn_score: Optional[int]


@dataclass_json
@dataclass
class Article:
    id: uuid.UUID
    title: str
    description: Optional[str]
    link: str
    score: float
    created_date: str
    modified_date: str
    article_data_sources: List[ArticleDataSource]
