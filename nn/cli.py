from typing import Any, Optional

import rich_click as click
from rich import print
from rich.console import Console

from nn.sources.service import get_and_show_sources

from .articles.service import get_and_show_articles
from .constants import DEFAULT_PAGE_SIZE
from .util import click_async


def common_options(func: Any) -> Any:
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
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs)

    return wrapper


@click.group()
@common_options
def app(debug: bool, number: int, page: int) -> None:
    if debug:
        print("Debug mode enabled")

    pass


@click.command("sources")  # type: ignore
@click_async
async def list_sources(debug: bool, number: int, page: int) -> None:
    """
    Lists sources you can query on specifically or find out more information
    about which sources this CLI serves up.
    """
    console = Console()
    with console.status("Loading..."):
        results = await get_and_show_sources(debug=debug)
        console.print(results)
        return


async def common_list_entry(debug: bool, number: int, page: int) -> None:
    if debug:
        print("Debug mode enabled")

    console = Console()
    with console.status("Loading..."):
        results = await get_and_show_articles(debug=debug, page=page - 1, number=number)
        console.print(results)
        return


@click.command(
    "all",
    help="""
    Consolidates all news entries by popular news sources and de-duplicates them when a common
    source is encountered (ex: HackerNews, Reddit, Lobste.rs, etc.)
    """,
)  # type: ignore
@common_options
@click_async
async def list_articles(debug: bool, number: int, page: int) -> None:
    return await common_list_entry(debug, number, page)


@click.command("hn", help="List news entries only from Hacker News")  # type: ignore
@common_options
@click_async
async def list_hn(debug: bool, number: int, page: int) -> None:
    return await common_list_entry(debug, number, page)


app.add_command(list_sources)
app.add_command(list_articles)
app.add_command(list_hn)


if __name__ == "__main__":
    app()
