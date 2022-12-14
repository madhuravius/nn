import os

BASE_NEWS_URL = os.getenv("BASE_NEWS_URL", "https://news.madhu.dev")
BASE_HACKERS_NEWS_PAGE_URL = "https://news.ycombinator.com/item?id="
BASE_LOBSTERS_PAGE_URL = "https://lobste.rs/s/"
BASE_REDDIT_PAGE_URL = "https://reddit.com/r/"

HN_LABEL = f"[bold #d1cfcc on #b84a00]HN[/]"
LOBSTERS_LABEL = "🦞"
REDDIT_LABEL = f"[bold #ffffff on #ff4500]Re[/]"

DEFAULT_PAGE_SIZE = 10
