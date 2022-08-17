from typing import Any, Optional

import rich_click as click
from rich import print
from rich.console import Console

from nn.sources.service import get_and_show_sources

from .articles.service import get_and_show_articles
from .constants import DEFAULT_PAGE_SIZE
from .util import click_async


@click.group()
def app() -> Optional[Any]:
    pass


@click.command("sources")
@click.option(
    "--debug",
    "-d",
    default=False,
    is_flag=True,
    help="""Enable debug mode.
    Newlines are removed by default.
    Double newlines are preserved.""",
)
@click_async
async def list_sources(debug: bool) -> None:
    """
    Lists sources you can query on specifically or find out more information
    about which sources this CLI serves up.
    """
    if debug:
        print("Debug mode enabled")

    console = Console()
    with console.status("Loading..."):
        results = await get_and_show_sources(debug=debug)
        console.print(results)
        return


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
    "--number",
    "-n",
    default=DEFAULT_PAGE_SIZE,
    help="""Specify number of articles to
    display per page.""",
)
@click.option(
    "--page",
    "-p",
    default=0,
    help="""Specify page number to retrieve
    data. This is based around a 1-index.""",
)
@click_async
async def list_articles(debug: bool, number: int, page: int) -> None:
    """
    Consolidates all news entries by popular news sources and de-duplicates them when a common
    source is encountered (ex: HackerNews, Reddit, Lobste.rs, etc.)
    """
    if debug:
        print("Debug mode enabled")

    console = Console()
    with console.status("Loading..."):
        results = await get_and_show_articles(debug=debug, page=page, page_size=number)
        console.print(results)
        return


app.add_command(list_sources)
app.add_command(list_articles)


if __name__ == "__main__":
    app()
