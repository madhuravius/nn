from typing import Any, Optional

import rich_click as click
from rich import print
from rich.console import Console

from nn.sources.service import get_and_show_sources

from .articles.service import get_and_show_articles
from .constants import DEFAULT_PAGE_SIZE
from .util import click_async

# Use Rich markup
click.rich_click.USE_RICH_MARKUP = True
COMMON_APPLY_TEXT = """Applies to:  [yellow]all[/], [yellow]hn[/], [yellow]lobsters[/yellow] and
[yellow]reddit[/]."""


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
        help=f"Specify number of articles to display per page. {COMMON_APPLY_TEXT}",
    )
    @click.option(
        "--page",
        "-p",
        default=0,
        help=f"Specify page number to retrieve data. This is based around a 1-index. "
        f"{COMMON_APPLY_TEXT}",
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


@click.command(  # type: ignore
    "sources",
    help="News sources that power this app. Run this to see where news is fed in from.",
)
@common_options
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


async def common_list_entry(
    debug: bool, filters: Optional[str], number: int, page: int
) -> None:
    if debug:
        print("Debug mode enabled")

    console = Console()
    with console.status("Loading..."):
        results = await get_and_show_articles(
            debug=debug, raw_filters=filters or [], page=page - 1, number=number
        )
        console.print(results)
        return


@click.command(  # type: ignore
    "all",
    help="""
    Consolidates all news entries by popular news sources and de-duplicates them when a common
    source is encountered (ex: HackerNews, Reddit, Lobste.rs, etc.)
    """,
)
@click.option(
    "--filter-sources",
    "-fs",
    default="",
    help=f"Pass in a set of filter sources in a csv way. Example: "
    f"--filter-sources hn,lobsters",
)
@common_options
@click_async
async def list_articles(
    debug: bool, filter_sources: str, number: int, page: int
) -> None:
    return await common_list_entry(debug, filter_sources.split(","), number, page)


@click.command("hn", help="List news entries only from Hacker News")  # type: ignore
@common_options
@click_async
async def list_hn(debug: bool, number: int, page: int) -> None:
    return await common_list_entry(debug, ["hn"], number, page)


@click.command("lobsters", help="List news entries only from Lobste.rs")  # type: ignore
@common_options
@click_async
async def list_lobsters(debug: bool, number: int, page: int) -> None:
    return await common_list_entry(debug, ["lobsters"], number, page)


@click.command("reddit", help="List news entries only from Reddit")  # type: ignore
@common_options
@click_async
async def list_reddit(debug: bool, number: int, page: int) -> None:
    return await common_list_entry(debug, ["reddit"], number, page)


app.add_command(list_sources)
app.add_command(list_articles)
app.add_command(list_hn)
app.add_command(list_lobsters)
app.add_command(list_reddit)


if __name__ == "__main__":
    app()
