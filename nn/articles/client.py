import http
import json

import httpx
from httpx import ConnectError
from rich import print_json

from ..constants import BASE_NEWS_URL
from ..models import Results


async def get_article_list(debug: bool, page: int, page_size: int) -> Results:
    async with httpx.AsyncClient() as client:
        try:
            results = await client.get(
                f"{BASE_NEWS_URL}/api/v1/articles?"
                f"sort=score,desc&sort=createdDate,desc&page={max(0, page)}&size={page_size}"
            )

            if debug:
                print_json(json=str(results.content.decode()))

            if results.status_code == http.HTTPStatus.OK:
                return Results.from_json(results.content)
        except ConnectError:
            return Results.from_json(
                json.dumps({"error": "Unable to connect to server."})
            )
