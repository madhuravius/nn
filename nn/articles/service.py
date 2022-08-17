from typing import Optional, Union

from rich.layout import Layout
from rich.table import Table

from .view import generate_results_table


async def get_and_show_articles(
    debug: bool, number: int, page: int
) -> Optional[Union[Layout, Table]]:
    _, table = await generate_results_table(debug, number, page)
    return table
