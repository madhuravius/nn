import asyncio
from typing import Any, Dict, Optional, Tuple, cast

from rich.table import Table

from .. import client
from ..constants import BASE_NEWS_URL, HN_LABEL, LOBSTERS_LABEL
from ..models import Results
from .models import DataSource


def get_label_from_name(name: str) -> str:
    if name == "Hacker News":
        return HN_LABEL
    elif name == "Lobste.rs":
        return LOBSTERS_LABEL
    return ""


async def generate_sources_table(
    debug: bool,
) -> Tuple[Optional[Results], Optional[Table]]:
    url = f"{BASE_NEWS_URL}/api/v1/data_sources"
    raw_results = await asyncio.gather(asyncio.sleep(1), client.get(debug, url))
    results = client.extract_results_from_call(raw_results)
    if not results or not results.content:
        return None, None

    table = Table(title="Data Sources", box=None, row_styles=["on #333333", ""])
    table.add_column()
    table.add_column()
    table.add_column()
    table.add_column()
    table.add_column()
    for idx, raw_row in enumerate(results.content):
        row: DataSource = DataSource.from_dict(cast(Dict[str, Any], raw_row))
        table.add_row(
            f"\n{get_label_from_name(row.name)}",
            f"\n{row.name}\n",
            f"\n{row.description}\n",
            f"\n[link={row.link}]Link[/link]\n",
        )

    return results, table
