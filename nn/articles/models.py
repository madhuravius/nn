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

    lobsters_author: Optional[str] = None
    lobsters_comment_count: Optional[int] = None
    lobsters_score: Optional[int] = None
    lobsters_short_id: Optional[str] = None


@dataclass_json
@dataclass
class ArticleSource(DataClassJsonMixin):
    id: uuid.UUID
    name: str
    link: str


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
    article_source: ArticleSource
    article_data_sources: List[ArticleDataSource]
