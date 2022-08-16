import asyncio
from typing import Optional, Tuple

from rich.table import Table

from ..constants import BASE_HACKERS_NEWS_PAGE_URL
from ..models import Results
from .client import get_article_list


async def generate_results_table(
    debug: bool, page: int, page_size: int
) -> Optional[Tuple[Optional[Results], Optional[Table]]]:
    raw_results = await asyncio.gather(
        asyncio.sleep(0.5), get_article_list(debug, page - 1, page_size)
    )
    if not raw_results:
        return None, print("No results found.")

    _, results = raw_results
    if results.error:
        return None, print(results.error)

    table = Table(title="News Now", box=None)
    table.add_column()
    table.add_column("Title", justify="left", style="cyan", no_wrap=True)
    table.add_column("💬 Comments", justify="left")
    table.add_column("🏆 Scores", justify="left")
    for idx, row in enumerate(results.content):
        metadata_comments = ""
        metadata_scores = ""
        if row.article_data_sources:
            for article_data_source in row.article_data_sources:
                if article_data_source.hn_id:
                    hn_link = f"{BASE_HACKERS_NEWS_PAGE_URL}{article_data_source.hn_id}"

                    metadata_comments += f"HN: [link={hn_link}]{article_data_source.hn_descendants}[/link]"
                    metadata_scores += f"HN: {article_data_source.hn_score}"
        table.add_row(
            str(idx + (1 + (results.number * results.size))),
            f"[link={row.link}]{row.title}[/link]",
            metadata_comments,
            metadata_scores,
        )
    return results, table
