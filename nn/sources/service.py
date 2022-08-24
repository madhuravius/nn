from typing import Optional

from rich.table import Table

from nn.sources.view import generate_sources_table


async def get_and_show_sources(
    debug: bool,
) -> Optional[Table]:
    _, table = await generate_sources_table(debug)
    return table
