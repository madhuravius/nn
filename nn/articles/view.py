import asyncio
from typing import Any, Dict, Optional, Tuple, cast

import arrow
from rich import print
from rich.table import Table

from .. import client
from ..constants import (
    BASE_HACKERS_NEWS_PAGE_URL,
    BASE_LOBSTERS_PAGE_URL,
    BASE_NEWS_URL,
    BASE_REDDIT_PAGE_URL,
    HN_LABEL,
    LOBSTERS_LABEL,
    REDDIT_LABEL,
)
from ..models import Results
from .models import Article, ArticleDataSource


def add_newlines_for_row_entries(
    metadata_comments: str,
    metadata_scores: str,
) -> Tuple[str, str]:
    if metadata_comments != "":
        metadata_comments += "\n"
    if metadata_scores != "":
        metadata_scores += "\n"
    return metadata_comments, metadata_scores


def add_hn_data(
    article_data_source: ArticleDataSource,
    metadata_comments: str,
    metadata_scores: str,
) -> Tuple[str, str]:
    if article_data_source.hn_id:
        metadata_comments, metadata_scores = add_newlines_for_row_entries(
            metadata_comments, metadata_scores
        )

        hn_link = f"{BASE_HACKERS_NEWS_PAGE_URL}{article_data_source.hn_id}"

        metadata_comments += (
            f"{HN_LABEL} [link={hn_link}]"
            f"{article_data_source.hn_descendants}[/link]"
        )
        metadata_scores += f"{HN_LABEL} {article_data_source.hn_score}"
    return metadata_comments, metadata_scores


def add_lobsters_data(
    article_data_source: ArticleDataSource,
    metadata_comments: str,
    metadata_scores: str,
) -> Tuple[str, str]:
    if article_data_source.lobsters_short_id:
        metadata_comments, metadata_scores = add_newlines_for_row_entries(
            metadata_comments, metadata_scores
        )

        lobsters_link = (
            f"{BASE_LOBSTERS_PAGE_URL}{article_data_source.lobsters_short_id}"
        )

        metadata_comments += (
            f"{LOBSTERS_LABEL} [link={lobsters_link}]"
            f"{article_data_source.lobsters_comment_count}[/link]"
        )
        metadata_scores += f"{LOBSTERS_LABEL} {article_data_source.lobsters_score}"
    return metadata_comments, metadata_scores


def add_reddit_data(
    article_data_source: ArticleDataSource,
    metadata_comments: str,
    metadata_scores: str,
) -> Tuple[str, str]:
    if article_data_source.reddit_name:
        metadata_comments, metadata_scores = add_newlines_for_row_entries(
            metadata_comments, metadata_scores
        )

        reddit_link_suffix = article_data_source.reddit_name.replace(
            f"{article_data_source.reddit_kind}_", ""
        )
        reddit_link = f"{BASE_REDDIT_PAGE_URL}{article_data_source.reddit_subreddit}/comments/{reddit_link_suffix}"

        metadata_comments += (
            f"{REDDIT_LABEL} [link={reddit_link}]"
            f"{article_data_source.reddit_num_comments}[/link]"
        )
        metadata_scores += f"{REDDIT_LABEL} {article_data_source.reddit_score}"
    return metadata_comments, metadata_scores


async def generate_results_table(
    debug: bool, csv_filters: str, number: int, page: int
) -> Tuple[Optional[Results], Optional[Table]]:
    url = f"{BASE_NEWS_URL}/api/v1/articles"
    if csv_filters:
        # sub endpoint within articles to capture more filtered posts
        url += "/search"
    url += f"?sort=score,desc&sort=createdDate,desc&page={max(0, page)}&size={number}"

    if csv_filters:
        url += f"&dataSources={csv_filters}"

    if debug:
        print(f"Querying URL: [blue]{url}[/]")

    raw_results = await asyncio.gather(asyncio.sleep(1), client.get(debug, url))
    results = client.extract_results_from_call(raw_results)
    if not results or not results.content:
        return None, None

    table = Table(title="News Now", box=None, row_styles=["on #333333", ""])
    table.add_column()
    table.add_column("Title", justify="left", style="cyan")
    table.add_column("????", justify="left")
    table.add_column("???? Scores", justify="left")
    for idx, raw_row in enumerate(results.content):
        row = Article.from_dict(cast(Dict[str, Any], raw_row))
        metadata_comments = ""
        metadata_scores = ""
        if row.article_data_sources:
            for article_data_source in sorted(
                row.article_data_sources, key=lambda d: d.id.data_source_id
            ):
                metadata_comments, metadata_scores = add_hn_data(
                    article_data_source, metadata_comments, metadata_scores
                )
                metadata_comments, metadata_scores = add_lobsters_data(
                    article_data_source, metadata_comments, metadata_scores
                )
                metadata_comments, metadata_scores = add_reddit_data(
                    article_data_source, metadata_comments, metadata_scores
                )

        created_date = arrow.get(row.created_date)

        title_col = f"[bold][link={row.link}]{row.title}[/link][/]"
        title_col += f"\n[white][italic]{created_date.humanize()}[/], {row.article_source.name}[/]"

        table.add_row(
            str(idx + (1 + (results.number * results.size))),  # type: ignore
            title_col,
            metadata_comments,
            metadata_scores,
        )
    return results, table
