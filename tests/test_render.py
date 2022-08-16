import json
import uuid

from faker import Faker
from pytest_httpx import HTTPXMock
from rich.console import Console

from nn.articles.models import Article, ArticleSource
from nn.articles.service import get_and_show_articles
from nn.models import Results


async def test_render(httpx_mock: HTTPXMock):
    fake = Faker()
    name = fake.name()
    httpx_mock.add_response(json=json.loads(Results(
        content=[Article(
            id=uuid.uuid4(),
            title=name,
            description=fake.company(),
            link=fake.url(),
            score=99,
            created_date=fake.date(),
            modified_date=fake.date(),
            article_source=ArticleSource(
                id=uuid.uuid4(),
                name=fake.name(),
                link=fake.url()
            ),
            article_data_sources=[]
        )],
        number=0,
        last=False,
        size=20,
    ).to_json()))
    console = Console(record=True)
    console.print(await get_and_show_articles(
        debug=False,
        page=0,
        page_size=5
    ))
    output = console.export_text()
    assert name in output
