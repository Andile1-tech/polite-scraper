from datetime import datetime, timezone
from pathlib import Path
from time import sleep
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from parser import discover_book_urls


CACHE_DIR = Path("cache/books")

HEADERS = {
    "User-Agent": "FlyRankInternship-A9/1.0"
}

TIMEOUT = 10
DELAY_SECONDS = 0.5


def cache_path(product_url):
    path = urlparse(product_url).path
    filename = path.strip("/").replace("/", "_") + ".html"
    return CACHE_DIR / filename


def fetch_detail_page(product_url):
    """
    Fetch one detail page.

    Cached pages are read locally.

    Network failures:
    - timeout: retry once
    - HTTP 5xx: retry once
    - HTTP 403/404: do not retry
    """

    cache_file = cache_path(product_url)

    if cache_file.exists():
        return (
            cache_file.read_text(
                encoding="utf-8"
            ),
            True,
        )

    attempts = 0

    while attempts < 2:
        attempts += 1

        try:
            sleep(DELAY_SECONDS)

            response = requests.get(
                product_url,
                headers=HEADERS,
                timeout=TIMEOUT,
            )

            if response.status_code in (403, 404):
                raise RuntimeError(
                    f"Failed to fetch {product_url}: "
                    f"HTTP {response.status_code}"
                )

            if 500 <= response.status_code <= 599:
                if attempts < 2:
                    print(
                        f"HTTP {response.status_code} "
                        f"for {product_url} - retrying once"
                    )
                    continue

                raise RuntimeError(
                    f"Failed to fetch {product_url}: "
                    f"HTTP {response.status_code}"
                )

            response.raise_for_status()

            CACHE_DIR.mkdir(
                parents=True,
                exist_ok=True,
            )

            cache_file.write_text(
                response.text,
                encoding="utf-8",
            )

            return (
                response.text,
                False,
            )

        except requests.Timeout:
            if attempts < 2:
                print(
                    f"Timeout for {product_url} "
                    f"- retrying once"
                )
                continue

            raise RuntimeError(
                f"Timeout fetching {product_url} "
                f"after 2 attempts"
            )

    raise RuntimeError(
        f"Failed to fetch {product_url}"
    )


def extract_book(
    product_url,
    source_page,
):
    html, cache_hit = fetch_detail_page(
        product_url
    )

    soup = BeautifulSoup(
        html,
        "html.parser",
    )

    product_main = soup.select_one(
        ".product_main"
    )

    if product_main is None:
        raise ValueError(
            f"Product area not found: "
            f"{product_url}"
        )

    title_element = product_main.select_one(
        "h1"
    )

    price_element = product_main.select_one(
        ".price_color"
    )

    availability_element = (
        product_main.select_one(
            ".availability"
        )
    )

    rating_element = product_main.select_one(
        "p.star-rating"
    )

    description_element = soup.select_one(
        "#product_description + p"
    )

    rating_text = None

    if rating_element:
        classes = rating_element.get(
            "class",
            [],
        )

        for class_name in classes:
            if class_name != "star-rating":
                rating_text = class_name
                break

    description = None

    if description_element:
        description = (
            description_element.get_text(
                " ",
                strip=True,
            )
        )

    record = {
        "title": (
            title_element.get_text(
                strip=True
            )
            if title_element
            else None
        ),
        "product_url": product_url,
        "price_text": (
            price_element.get_text(
                strip=True
            )
            if price_element
            else None
        ),
        "availability_text": (
            availability_element.get_text(
                " ",
                strip=True,
            )
            if availability_element
            else None
        ),
        "rating_text": rating_text,
        "description": description,
        "source_page": source_page,
        "fetched_at": datetime.now(
            timezone.utc
        ).isoformat(),
    }

    return record, cache_hit


def extract_all_books():
    """
    Extract all discovered books.

    One failed detail page does not stop
    the remaining books from being processed.
    """

    books = []
    failures = []

    detail_pages = 0
    cache_hits = 0

    discovered_books = discover_book_urls()

    for product_url, source_page in discovered_books:

        try:
            record, cache_hit = extract_book(
                product_url,
                source_page,
            )

            books.append(record)
            detail_pages += 1

            if cache_hit:
                cache_hits += 1

            print(
                f"Extracted "
                f"{len(books)}/"
                f"{len(discovered_books)}: "
                f"{record['title']}"
            )

        except Exception as exc:
            failure = {
                "product_url": product_url,
                "source_page": source_page,
                "error": str(exc),
            }

            failures.append(failure)

            print(
                f"FAILED "
                f"{product_url}: {exc}"
            )

    print()
    print(
        f"detail_pages={detail_pages}"
    )
    print(
        f"cache_hits={cache_hits}"
    )
    print(
        f"failed_pages={len(failures)}"
    )

    if books:
        print()
        print("First raw record:")
        print(books[0])

    return (
        books,
        {
            "pages_fetched": detail_pages,
            "cache_hits": cache_hits,
            "failures": failures,
        },
    )


if __name__ == "__main__":
    raw_books, stats = extract_all_books()

    print()
    print("Extraction complete.")
    print(
        f"Successful records: "
        f"{len(raw_books)}"
    )
    print(
        f"Failed pages: "
        f"{len(stats['failures'])}"
    )