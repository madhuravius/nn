from os import get_terminal_size
from typing import Any, Optional

import rich_click as click
from rich import print
from rich.console import Console

from .articles.service import get_and_show_articles
from .util import click_async


@click.group()
def app() -> Optional[Any]:
    pass


@click.command("all")  # type: ignore
@click.option(
    "--debug",
    "-d",
    default=False,
    is_flag=True,
    help="""Enable debug mode.
    Newlines are removed by default.
    Double newlines are preserved.""",
)
@click.option(
    "--page",
    "-p",
    default=0,
    help="""Specify page number to retrieve
    data. This is based around a 1-index.""",
)
@click_async
async def list_articles(debug: bool, page: int) -> None:
    """
    This consolidates all news entries by popular news sources and de-duplicates them when a common
    source is encountered (ex: HackerNews, Reddit, Lobste.rs, etc.)
    """
    if debug:
        print("Debug mode enabled")

    page_size = get_terminal_size().lines - 5
    console = Console()
    results = await get_and_show_articles(debug=debug, page=page, page_size=page_size)
    console.print(results)
    return


app.add_command(list_articles)


if __name__ == "__main__":
    app()
