from typing import Optional, Union

from rich.layout import Layout
from rich.table import Table

from .view import generate_results_table


async def get_and_show_articles(
    debug: bool, page: int, page_size: int = 20
) -> Optional[Union[Layout, Table]]:
    _, table = await generate_results_table(debug, page, page_size)
    return table
