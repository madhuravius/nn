import http
import json
from typing import Any, Optional

import httpx
from httpx import ConnectError
from rich import print_json

from .models import Results


def extract_results_from_call(raw_results) -> Optional[Results]:
    if not raw_results:
        print("No results found.")
        return None

    _, results = raw_results
    if results.error:
        print(results.error)
        return None

    if not type(results) == Results or not results.content:
        print("No results found")
        return None

    return results


async def get(debug: bool, url: str) -> Any:
    async with httpx.AsyncClient() as client:
        try:
            results = await client.get(url)

            if debug:
                print_json(json=str(results.content.decode()))

            if results.status_code == http.HTTPStatus.OK:
                return Results.from_json(results.content)
            else:
                return Results.from_json(
                    json.dumps(
                        {
                            "error": f"Unable to connect to server with code {results.status_code}."
                        }
                    )
                )
        except ConnectError:
            return Results.from_json(
                json.dumps({"error": "Unable to connect to server."})
            )
