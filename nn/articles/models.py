import uuid
from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import DataClassJsonMixin, dataclass_json


@dataclass_json
@dataclass
class ArticleDataSourceId(DataClassJsonMixin):
    article_id: uuid.UUID
    data_source_id: uuid.UUID


@dataclass_json
@dataclass
class ArticleDataSource(DataClassJsonMixin):
    id: ArticleDataSourceId

    hn_by: Optional[str] = None
    hn_descendants: Optional[int] = None
    hn_id: Optional[int] = None
    hn_score: Optional[int] = None

    lobsters_author: Optional[str] = None
    lobsters_comment_count: Optional[int] = None
    lobsters_score: Optional[int] = None
    lobsters_short_id: Optional[str] = None

    reddit_author: Optional[str] = None
    reddit_kind: Optional[str] = None
    reddit_name: Optional[str] = None
    reddit_num_comments: Optional[int] = None
    reddit_permalink: Optional[str] = None
    reddit_score: Optional[int] = None
    reddit_sub_reddit: Optional[str] = None


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
