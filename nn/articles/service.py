from typing import Any, Dict, List, Optional, cast

from rich import print
from rich.table import Table

from .. import client
from ..constants import BASE_NEWS_URL
from ..sources.models import DataSource
from .view import generate_results_table


async def get_and_show_articles(
    debug: bool, raw_filters: Optional[List[str]], number: int, page: int
) -> Optional[Table]:
    if raw_filters:
        url = f"{BASE_NEWS_URL}/api/v1/data_sources"
        raw_results = await client.get(debug, url)
        results = client.extract_results_from_call((None, raw_results))
        if not results or not results.content:
            print("Unable to find any results by filters entered")
            return None

        pre_csv_filters = []
        for result in results.content:
            data_source = DataSource.from_dict(cast(Dict[str, Any], result))
            for raw_filter in raw_filters:
                if raw_filter == data_source.metadata.group_as:
                    pre_csv_filters.append(str(data_source.id))
        filters = ",".join(pre_csv_filters)

    else:
        filters = ""

    _, table = await generate_results_table(debug, filters, number, page)
    return table
