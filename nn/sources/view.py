import asyncio
from typing import Any, Dict, Optional, Tuple, cast

from rich.table import Table

from .. import client
from ..constants import BASE_NEWS_URL, HN_LABEL, LOBSTERS_LABEL, REDDIT_LABEL
from ..models import Results
from .models import DataSource


def get_label_from_group_as(group_as: Optional[str]) -> str:
    if group_as == "hn":
        return HN_LABEL
    elif group_as == "lobsters":
        return LOBSTERS_LABEL
    elif group_as == "reddit":
        return REDDIT_LABEL
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
    content = []
    for raw_row in results.content:
        content.append(DataSource.from_dict(cast(Dict[str, Any], raw_row)))

    for idx, row in enumerate(sorted(content, key=lambda d: d.name)):
        table.add_row(
            f"\n{get_label_from_group_as(row.metadata.group_as)}",
            f"\n{row.name}\n",
            f"\n{row.description}\n",
            f"\n[link={row.link}]Link[/link]\n",
        )

    return results, table
